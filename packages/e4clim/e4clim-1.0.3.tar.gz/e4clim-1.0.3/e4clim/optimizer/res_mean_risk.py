"""Renewable-energy mean-risk optimization module."""
import os
from collections import OrderedDict
from itertools import product
from copy import deepcopy
import logging
import numpy as np
import pandas as pd
import xarray as xr
from scipy.optimize import Bounds, minimize
from cvxopt import solvers, matrix, spmatrix
import matplotlib.pyplot as plt
from matplotlib import rcParams, ticker
from ..container import ensure_collection
from ..optimization import OptimizerBase, SolutionBase, InputBase
from ..plot import plot_geo_dist
from ..config import load_config


#: Logger.
log = logging.getLogger(__name__)


class Optimizer(OptimizerBase):
    """Renewable energy mean risk optimizer."""

    def __init__(self, med, cfg=None, **kwargs):
        """Constructor setting input data period used.

        :param med: Mediator.
        :param cfg: Optimizer configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type cfg: dict

        .. seealso:: :py:class:`.optimization.OptimizerBase`.
        """
        super(Optimizer, self).__init__(
            med, 'res_mean_risk', cfg=cfg, **kwargs)

        # Add demand and generation components
        self.demand_component = self.med.components[
            self.cfg['component']['demand']]
        self.generation_component = {
            comp_name: self.med.components[comp_name]
            for comp_name in self.cfg['component']['capacity_factor']}

        # Number of generation components
        self.n_gen_comp = len(self.generation_component)

        # Overwrite input and solution with module class
        self.input = Input(self, self.cfg['input'], **kwargs)
        self.solution = Solution(self, self.cfg, **kwargs)

        # Add cases to solve in solution variables
        self.cases = {}
        self.case_keys = self.cfg.pop('cases')
        self.add_cases(**kwargs)

        # Add reference capacity data source
        variable = 'capacity'
        for src_name in self.cfg['reference_{}'.format(variable)].values():
            self.med.add_data_source(src_name, variables=variable)

    def add_cases(self, **kwargs):
        """Add cases to solution variables."""
        cases_values = []
        prop_names = []
        for keys_orig in self.case_keys:
            keys = keys_orig.copy()
            prop_names.append(keys[-1])
            value = self.cfg
            while len(keys) > 0:
                key = keys.pop(0)
                value = value[key]
            cases_values.append(ensure_collection(value))

        # Product of cases
        cases_prod = product(*cases_values)
        variables = set()
        for k, values in enumerate(cases_prod):
            case_name = ''.join([n + str(v)
                                 for (n, v) in zip(prop_names, values)])
            variables.add(case_name)
            self.cases[case_name] = values
        # Add variables to solution
        self.solution.update_variables(variables, **kwargs)

    def solve(self, **kwargs):
        """Solve optimization problem for all cases."""
        for case_name, case_values in self.cases.items():
            if not self.cfg.get('no_verbose'):
                log.info('Optimizing case {}:'.format(case_name))
            # Configure case
            cfg_case = deepcopy(self.cfg)
            for k, keys_orig in enumerate(self.case_keys):
                # Manage keys tree
                keys = keys_orig.copy()
                cfg_entry = cfg_case
                while len(keys) > 1:
                    key = keys.pop(0)
                    cfg_entry = cfg_entry[key]
                # Set value of each case key
                cfg_entry[keys[0]] = case_values[k]
                if not self.cfg.get('no_verbose'):
                    log.info('  - with {} = {}'.format(
                        keys[0], cfg_entry[keys[0]]))

            # Get solution for each case
            self.solution.update({
                case_name: self.solve_case(cfg_case, **kwargs)})

    def solve_case(self, cfg_case, **kwargs):
        """Solve optimization problem for a specific case.

        :param cfg_case: Case configuration.
        :type cfg_case: dict

        :returns: Solution.
        :rtype: dict
        """
        # Convert some scalars
        dim_comp_reg_name = 'component_region'
        n_comp_reg = int(self.input['n_comp_reg'])
        max_capacity = float(cfg_case['grid']['max_capacity'])
        min_capacity = float(cfg_case['grid']['min_capacity'])
        dem_tot_mean = float(self.input['dem_mean'].sum('region'))

        # Get total capacity
        ref_tot_cap = self.get_reference_total_capacity(**kwargs)

        # Bounds on capacity
        if cfg_case['cstr']['bounds']:
            bounds = Bounds(min_capacity, max_capacity)
        else:
            bounds = None

        # Shortage, saturation and pv fraction arguments
        max_conventional = np.percentile(
            self.input['dem'].sum('region'),
            cfg_case['grid']['max_conventional'] * 100)
        args_shortage = (
            self.input['cf'].transpose('time', dim_comp_reg_name).values,
            self.input['dem'].transpose('time', 'region').values,
            max_conventional)
        args_saturation = (
            self.input['cf'].transpose('time', dim_comp_reg_name).values,
            self.input['dem'].transpose('time', 'region').values,
            cfg_case['grid']['max_res'])
        args_pv_frac = (0.,)

        # Mask covariance matrix
        mask_cov = self._get_mask_cov(cfg_case['strategy'])
        cf_cov = self.input['cf_cov'].values
        cf_cov_masked = self.input['cf_cov'].where(~ mask_cov, 0.).values

        # List of objective function
        args = [(cf_cov_masked,)]
        funs, jacs, weights = [fun_var], [jac_var], [1.]

        # Add total capacity constraint
        args_tot_cap = (ref_tot_cap,)
        if isinstance(cfg_case['cstr']['tot_cap'], bool):
            # Hard constraint
            if cfg_case['cstr']['tot_cap']:
                tot_cap_cstr = {
                    'type': 'eq', 'fun': fun_tot_cap,
                    'jac': jac_tot_cap, 'args': args_tot_cap}
        else:
            # Soft constraint
            funs.append(fun_tot_cap_squared)
            jacs.append(jac_tot_cap_squared)
            args.append(args_tot_cap)
            weights.append(cfg_case['cstr']['tot_cap'])

        # Collect objective functions and jacobians as a weighted sum
        fun = fun_collector(funs, weights)
        jac = fun_collector(jacs, weights)

        # Solve multi-objective problem by setting a
        # target penetration rate
        target_mean_pen_rng = np.arange(cfg_case['penetration']['start'],
                                        cfg_case['penetration']['stop'],
                                        cfg_case['penetration']['step'])

        # Array of optimal capacities
        sol = xr.Dataset()
        dims = (target_mean_pen_rng.shape[0],)
        coord_pen = ('target_mean_penetration', target_mean_pen_rng * 100)
        coords = [coord_pen, (
            dim_comp_reg_name, self.input['cf'].coords[dim_comp_reg_name])]
        sol['region'] = self.input['dem'].coords['region']
        sol['capacity'] = xr.DataArray(
            np.empty(dims + (n_comp_reg,)), coords=coords).where(False)
        sol['generation'] = xr.DataArray(
            np.empty(dims + (n_comp_reg,)), coords=coords).where(False)
        sol['risk'] = xr.DataArray(np.empty(dims), coords=[
            coord_pen]).where(False)
        sol['mean_penetration'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        sol['profit'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        sol['pv_frac'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        sol['shortage'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        sol['saturation'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        sol['tot_cap'] = xr.DataArray(
            np.empty(dims), coords=[coord_pen]).where(False)
        coords = [coord_pen, self.input['cf'].coords['time'],
                  self.input['dem'].coords['region']]
        # sol['Pmismatch'] = xr.DataArray(
        #    np.empty(dims + (nt, n_reg)), coords=coords).where(False)
        # coords = [coord_pen, self.input['dem'].coords['region']]
        # PmismatchStd = xr.DataArray(
        #     np.empty(dims + (n_reg,)), coords=coords).where(False)

        # Conversion to GWh/y
        fact = 24 * 365 * 1e-6

        # Loop over range of targets
        for (imu, target_mean_pen) in enumerate(target_mean_pen_rng):
            # Define initial state
            try:
                # Use previous minimizer otherwise
                x0 = res.x
            except (NameError, AttributeError):
                # Use a uniform generation initial state for first iteration
                x0 = (np.ones((n_comp_reg,)) * target_mean_pen
                      * dem_tot_mean / n_comp_reg)

            # Collect constraints
            # SLSQP: constraints are defined as list of dictionaries
            # Total penetration constraint
            args_tot_pen = (self.input['cf_mean'].values,
                            target_mean_pen * dem_tot_mean)
            tot_pen_cstr = {'type': 'eq', 'fun': fun_total_penetration,
                            'jac': jac_total_penetration,
                            'args': args_tot_pen}

            # Collect constraints
            constraints = []
            if (isinstance(cfg_case['cstr']['tot_cap'], bool)
                    and cfg_case['cstr']['tot_cap']):
                # Hard constraint
                constraints.append(tot_cap_cstr)
            if cfg_case['cstr']['total_penetration']:
                constraints.append(tot_pen_cstr)

            # Solve problem
            # if not cfg_case.get('no_verbose'):
            #     log.info('- for a target mean penetration of '
            #              '{:.1f} %'.format(target_mean_pen * 100))
            res = minimize(fun, x0, args=args, jac=jac, bounds=bounds,
                           constraints=constraints, **cfg_case['scipy'])

            # Save results only if total penetration constraint not violated
            gap = -fun_total_penetration(res.x, *
                                         args_tot_pen) * 100 / dem_tot_mean
            if np.abs(gap) > 1.e-3:
                # if not cfg_case.get('no_verbose'):
                #     log.info('Total_penetration_constraint_violation: '
                #              '{:.2e} %'.format(gap))
                continue

            x = xr.DataArray(res.x, dims=(dim_comp_reg_name,))
            loc = {'target_mean_penetration': target_mean_pen * 100}
            sol['capacity'].loc[loc] = x
            sol['generation'].loc[loc] = (
                x * self.input['cf_mean'] * fact)
            sol['mean_penetration'].loc[loc] = (
                self.input['cf_mean'].dot(x) / dem_tot_mean)
            # Use full rather than masked covariance matrix when plotting
            # as opposed to when optimizing, so as for the risk to be
            # the same with/without interconnection (global/regional)
            sol['risk'].loc[loc] = np.sqrt(
                fun_var(x, cf_cov)) / dem_tot_mean
            pv_loc = (self.input['cf'].component == 'pv').values
            cstr_ratio = fun_pv_frac(
                res.x, pv_loc, args_pv_frac) / res.x.sum()
            sol['pv_frac'].loc[loc] = cstr_ratio + args_pv_frac[0]
            sol['shortage'].loc[loc] = shortage_frequency(
                res.x, *args_shortage)
            sol['saturation'].loc[loc] = saturation_frequency(
                res.x, *args_saturation)
            sol['tot_cap'].loc[loc] = res.x.sum()

            # # Print
            # if not cfg_case.get('no_verbose'):
            #     log.info('Found optimal capacities (MW): {}'.format(
            #         res.x.astype(int)))
            #     log.info('  Total capacity: {} MW'.format(
            #         int(sol['tot_cap'].loc[loc])))
            #     log.info('  Mean/Risk: {}'.format(
            #         (sol['mean_penetration']
            #          / sol['risk']).loc[loc].values))
            #     log.info(
            #         '  pv fraction: {:d} % ({} % more than target)'.format(
            #             int(sol['pv_frac'].loc[loc] * 100),
            #             int(cstr_ratio * 100)))
            #     log.info('  Shortage frequency: {} %'.format(
            #         int(sol['shortage'].loc[loc] * 100)))
            #     log.info('  Saturation frequency: {} %'.format(
            #         int(sol['saturation'].loc[loc] * 100)))

        # Add RES generation
        # PRES = (self.input['cf'] * sol['capacity']) * fact
        # coords = [coord_pen, self.input['cf'].coords['time'],
        #           self.input['dem'].coords['region']]
        # PRES = PRES.groupby(
        # PRES.coords[dim_comp_reg_name] % 6).sum(
        # dim_comp_reg_name, skipna=False)
        # del PRES['component'], PRES['region' + 'Multi']
        # PRES = (PRES.rename({dim_comp_reg_name: 'region'}).assign_coords(
        #     **{'region': self.input['dem'].coords['region']})
        #         .transpose('time', coord_pen[0], 'region'))
        # PRESMean = PRES.mean('time')
        # PRESStd = PRES.std('time')
        # sol['PRES'] = PRES

        # Add optimization configuration as attributes
        _save_dict(cfg_case, sol)

        return sol

    def _get_mask_cov(self, strategy):
        """Get covariance-matrix mask for a given strategy.

        :param strategy: Strategy (`'global'`, `'techno'`, or `'none'`)
        :type strategy: str

        :returns: Covariance-matrix mask.
        :rtype: :py:class:`xarray.DataArray`
        """
        dim_comp_reg_name = 'component_region'
        n_reg = int(self.input['n_reg'])
        n_comp_reg = self.n_gen_comp * n_reg

        mask_cov = xr.ones_like(self.input['cf_cov'], dtype=bool)
        if strategy == 'none':
            # Only the variances (diagnonal) are considered in the optimization
            idx = xr.DataArray(range(n_comp_reg),
                               dims=[dim_comp_reg_name + '_i'])
            mask_cov[idx, idx] = False
        elif strategy == 'techno':
            # Covariances between technologies of the same region
            for ic in range(self.n_gen_comp):
                i_diag = ic * n_reg + np.arange(n_reg)
                for jc in range(self.n_gen_comp):
                    j_diag = jc * n_reg + np.arange(n_reg)
                    mask_cov.values[(i_diag, j_diag)] = False
        elif strategy == 'global':
            # Both technological and regional covariances
            mask_cov[:] = False
        else:
            raise RuntimeError(
                'Invalid strategy choice: {}. Should be none, techno or '
                'global.'.format(strategy))

        return mask_cov

    def get_reference_total_capacity(self, capacity=None, **kwargs):
        """Get total capacity from `'grid'` configuration or from data file.

        :param capacity: Capacity array. Default is `None`, in which case
          capacities are concatenated from components output data source(s).
        :type capacity: :py:class:`xarray.DataArray`

        :returns: Total capacity.
        :dtype: float
        """
        if ('tot_cap' in self.cfg['grid']) and (not capacity):
            tot_cap = float(self.cfg['grid']['tot_cap'])
            if not self.cfg.get('no_verbose'):
                log.info('Read total capacity of {.0f} MW from '
                         'grid configuration'.format(tot_cap))
        else:
            # Get total capacity for each generation component
            da = (self.get_reference_capacity(**kwargs)[0]
                  if capacity is None else capacity)
            tot_cap = float(da.sum(['region', 'component']))
            if not self.cfg.get('no_verbose'):
                log.info('Read total capacity of {:.0f} MW from '
                         'generation data'.format(tot_cap))

        return tot_cap

    def get_reference_capacity(self, **kwargs):
        """Aggregate capacity for all generation components.

        :returns: Capacities and data sources postfix.
        :dtype: :py:class:`tuple` of :py:class:`xarray.DataArray` and
          :py:class:`str`
        """
        syear = '{}-12-31'.format(self.cfg['reference_year'])
        data = []
        variable = 'capacity'
        postfix = '_' + self.med.cfg['area']
        for comp in self.generation_component.values():
            # Read component reference capacity from given data source
            data_src = self.med.data_sources[
                self.cfg['reference_{}'.format(variable)][comp.name]]
            data_src.get_data(**kwargs)
            postfix += '_{}_{}{}'.format(
                comp.name, data_src.name,
                data_src.get_data_postfix(**kwargs))

            # Select
            comp_data = data_src[variable].sel(time=syear)
            try:
                # Try to select component (if multi-index)
                comp_data = comp_data.sel(component=comp.name)
            except ValueError:
                pass
            data.append(comp_data)

        # Add reference year to postfix
        postfix += '_' + self.cfg['reference_year']

        return (xr.concat(data, dim='component'), postfix)


class Input(InputBase):
    """Optimization problem input data-source."""

    def __init__(self, opt, cfg=None, **kwargs):
        """Initialize input data-source.

        :param opt: Optimizer.
        :param cfg: Input configuration. Default is `None`.
        :type opt: :py:class:`.optimization.OptimizerBase`
        :type cfg: dict
        """
        super(Input, self).__init__(opt, cfg=cfg, **kwargs)

        # Set input data period to use
        if self.cfg['select_period']:
            self.start_date = pd.Timestamp(self.cfg['start_date'])
            self.end_date = pd.Timestamp(self.cfg['end_date'])

    def download(self, **kwargs):
        pass

    def load(self, **kwargs):
        """Load optimization problem input data."""
        # Get output data (from prediction if estimator available
        # or directly from output data source)
        self.opt.demand_component.get_result()
        for comp in self.opt.generation_component.values():
            comp.get_result()

        # Read demand prediction
        da_dem = self.opt.demand_component.result[
            self.opt.cfg['component']['demand']]

        # Read capacity factors prediction
        da_list = []
        variable = 'capacity_factor'
        for comp in self.opt.generation_component.values():
            da_comp = comp.result[variable].expand_dims('component')
            da_list.append(da_comp)
        da_cf = xr.concat(da_list, dim='component')

        # Select period
        if self.cfg['select_period']:
            time_slice = slice(self.start_date, self.end_date)
            da_dem = da_dem.sel(time=time_slice)
            da_cf = da_cf.sel(time=time_slice)

        # Get common time slice and select
        common_index = da_dem.indexes['time']
        common_index = common_index.intersection(da_cf.indexes['time'])
        time_slice = slice(common_index[0], common_index[-1])
        da_dem = da_dem.sel(time=time_slice)
        da_cf = da_cf.sel(time=time_slice)
        if not self.cfg.get('no_verbose'):
            log.info('{}-{} period selected'.format(
                *da_cf.indexes['time'][[0, -1]].to_list()))

        # Collect data for global problem
        dim_comp_reg_name = 'component_region'

        ds = self._collect_data(da_dem, da_cf, **kwargs).reset_index(
            dim_comp_reg_name)

        return ds

    def _collect_data(self, da_dem, da_cf, **kwargs):
        """"Collect demand and capacity factor input data
        needed for regional RES distribution optimization problem.

        :param da_dem: Demand data array.
        :param da_cf: Capacity factors data array.
        :type da_dem: :py:obj:`xarray.DataArray`
        :type da_cf: :py:obj:`xarray.DataArray`

        :returns: Dataset collecting all necessary data.
        :rtype: :py:obj:`xarray.Dataset`
        """
        dim_comp_reg_name = 'component_region'
        dim_comp_reg = {dim_comp_reg_name: (
            'component', 'region_multi')}

        # Problem dimensions
        n_reg = len(da_cf.coords['region'])
        n_comp_reg = self.opt.n_gen_comp * n_reg

        # Make sure that demand regions follow the order of CF regions
        dem = da_dem.sel(region=da_cf.indexes['region'])

        # Convert daily energy (MWh/d) to power (MW)
        if self.med.cfg['frequency'] == 'day':
            dem /= 24
        dem.attrs['units'] = 'MW'

        # Concatenate components
        cf = da_cf.rename({'region': 'region_multi'}).stack(**dim_comp_reg)

        # Get time means
        dem_mean = dem.mean('time')
        cf_mean = cf.mean('time')
        dem_tot_mean = dem_mean.sum('region')

        # Normalized capacity factors (rescaled by total mean demand)
        cf_norm = da_cf.copy(deep=True) / dem.sum('region') * dem_tot_mean
        cf_norm = cf_norm.rename(
            {'region': 'region_multi'}).stack(**dim_comp_reg)

        # Covariance matrix of regional components
        cf_norm_valid = cf_norm.where(~cf_norm.isnull(), 0.)
        cf_cov = xr.DataArray(np.cov(cf_norm_valid, rowvar=False), coords=[
            (dim_comp_reg_name + '_i', range(n_comp_reg)),
            (dim_comp_reg_name + '_j', range(n_comp_reg))])

        cf_cov.attrs['long_name'] = 'Capacity Factor Covariance'
        cf_cov.attrs['long_name'] = 'Normalized {}'.format(
            cf_cov.attrs['long_name'])

        # Add long names
        cf.attrs['long_name'] = 'Capacity Factor Time Series'
        cf_mean.attrs['long_name'] = 'Capacity Factor Mean'
        dem.attrs['long_name'] = 'Demand'
        dem_mean.attrs['long_name'] = 'Mean Demand Mean'
        n_comp_reg = xr.DataArray(n_comp_reg)
        n_comp_reg.attrs['long_name'] = 'Number of Regions and Components'
        n_reg = xr.DataArray(n_reg)
        n_reg.attrs['long_name'] = 'Number of Regions'

        # Collect as Dataset
        ds = xr.Dataset(OrderedDict(
            n_comp_reg=n_comp_reg, n_reg=n_reg, cf=cf, cf_mean=cf_mean,
            cf_cov=cf_cov, dem=dem, dem_mean=dem_mean))

        return ds

    def get_data_postfix(self, **kwargs):
        """Get data postfix.

        :returns: Postfix.
        :rtype: str
        """
        # Get user-defined postfix
        postfix = self.cfg.get('postfix')

        if postfix is None:
            # Get standard postfix
            postfix = []

            # Demand postfix
            postfix.append(self.opt.demand_component['demand'].result.
                           get_data_postfix(**kwargs).split('_'))

            # Capacity factors postfix
            for comp in self.opt.generation_component.values():
                postfix.append(comp['capacity_factor'].result.
                               get_data_postfix(**kwargs).split('_'))

            # Join postfixes
            postfix = np.concatenate(postfix)
            _, idx = np.unique(postfix, return_index=True)
            postfix = '_'.join(postfix[np.sort(idx)])

            # Add period
            if self.cfg['select_period']:
                postfix += '_{}-{}'.format(
                    self.start_date.date().strftime('%Y%m%d'),
                    self.end_date.date().strftime('%Y%m%d'))

        return postfix

    def plot_reference_capacity(self, **kwargs):
        """Plot map of regional capacity from reference."""
        cfg_plot = load_config(self.med.cfg, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        map_dir = self.med.cfg.get_plot_directory(
            self.opt, subdirs='map', **kwargs)

        # Get reference capacity
        capa_ref, result_postfix = self.opt.get_reference_capacity(**kwargs)

        # Read the regions coordinates and ensure order
        self.med.geo_src.get_data()
        df_coords = self.med.geo_src.read_region_coordinates(**kwargs)
        df_coords = df_coords.loc[capa_ref['region'], :]
        lat, lon = df_coords['lat'].values, df_coords['lon'].values

        # Plot reference capacity
        if not cfg_plot.get('no_verbose'):
            log.info('Plotting reference capacity')
        capa_pv = capa_ref.sel(component='pv')
        capa_wind = capa_ref.sel(component='wind')
        fig_filename = 'map_capacity_reference{}.{}'.format(
            result_postfix, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind, **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)


class Solution(SolutionBase):
    def get_data_postfix(self, **kwargs):
        """Get optimization results postfix with constraints in addition
        to default postfix.

        :returns: Postfix.
        :rtype: str
        """
        # Get user-defined postfix
        postfix = self.cfg.get('postfix')

        if postfix is None:
            # Get default postfix
            postfix = super(Solution, self).get_data_postfix(**kwargs)

        return postfix

    def plot_mean_risk_front(self, **kwargs):
        """Plot mean-risk optimal frontiers of solutions."""
        optimal_only = True
        dim_comp_reg_name = 'component_region'
        dim_comp_reg = {dim_comp_reg_name: ('component', 'region_multi')}
        cfg_plot = load_config(self.med.cfg, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        front_dir = self.med.cfg.get_plot_directory(
            self.opt, subdirs='front', **kwargs)
        pv_frac_dir = self.med.cfg.get_plot_directory(
            self.opt, subdirs='pv_frac', **kwargs)
        result_postfixes = []

        # Get total capacity
        capa_ref, _ = self.opt.get_reference_capacity(**kwargs)
        ref_tot_cap = self.opt.get_reference_total_capacity(
            capa_ref, **kwargs)

        # Mean-risk plot options
        # tau_critic = 1.e-2
        tau_critic = 99.e-2
        msize = 6
        xlim = [0., 23.]
        colors = ['k'] + rcParams['axes.prop_cycle'].by_key()['color']
        ymin_ratio, ymax_ratio = 0., 100.

        # Make sure input data is loaded
        self.opt.input.get_data(**kwargs)
        pv_loc = self.opt.input['cf'].component == 'pv'

        # Set up the figures
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig_ratio = plt.figure()
        ax_ratio1 = fig_ratio.add_subplot(111)
        ax_ratio2 = ax_ratio1.twinx()

        dem_tot_mean = float(self.opt.input['dem_mean'].sum('region'))

        # Objective function and its arguments
        # Use full rather than masked covariance matrix when plotting
        # as opposed to when optimizing, so as for the risk to be
        # the same with/without interconnection (global/regional)
        args0 = (self.opt.input['cf_cov'].values,)
        fun0 = fun_var
        capa_ref = capa_ref.rename(
            {'region': 'region_multi'}).stack(**dim_comp_reg)

        # Get the mean penetration and the risk of the observed mix
        mean_penetration_obs = self.opt.input['cf_mean'].values.dot(
            capa_ref) / dem_tot_mean
        risk_obs = np.sqrt(fun0(capa_ref, *args0)) / dem_tot_mean
        pv_capa = capa_ref.loc[{dim_comp_reg_name: pv_loc}]
        pv_frac_obs = float(pv_capa.sum() / capa_ref.sum())
        ax_ratio1.scatter(mean_penetration_obs * 100, pv_frac_obs * 100,
                          s=msize**2, c=colors[2], marker='o', zorder=2)
        if not cfg_plot.get('no_verbose'):
            log.info('Observed mix:')
            log.info('  Mean total penetration: {:.1f} %'.format(
                mean_penetration_obs * 100))
            log.info('  Risk: {:.1f} %'.format(risk_obs * 100))
            log.info('  Mean-risk ratio: {:.3f}'.format(
                mean_penetration_obs / risk_obs))
            log.info('  pv fraction: {:.1f} %'.format(pv_frac_obs * 100))

        # Plot mean-risk point of observed mix
        ax.scatter(risk_obs * 100, mean_penetration_obs * 100,
                   s=msize**2, c=colors[-3], marker='o', zorder=2)

        # Plot global strategy
        cap_values = [False, True]
        strategy = 'global'
        for k, cap_val in enumerate(cap_values):
            if not cfg_plot.get('no_verbose'):
                log.info('{} mix:'.format(strategy))
            case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
            sol = self[case_name]
            result_postfixes.append(np.array(
                self.get_data_postfix().split('_')))

            # Plot on pv fraction
            idx_opt = np.arange(0, len(sol['target_mean_penetration']))
            if cap_val:
                # Get index of minimum risk under capacity constraint
                idx_min_risk = int(np.argmin(sol['risk']))
                if optimal_only:
                    idx_opt = np.arange(idx_min_risk, len(
                        sol['target_mean_penetration']))
                h_ratio = ax_ratio1.plot(
                    sol['target_mean_penetration'][idx_opt],
                    sol['pv_frac'][idx_opt] * 100,
                    linestyle='-', color=colors[2])[0]
                h_short = ax_ratio2.plot(
                    sol['target_mean_penetration'][idx_opt],
                    sol['shortage'][idx_opt] * 100,
                    linestyle='-', color=colors[3])[0]
                h_sat = ax_ratio2.plot(
                    sol['target_mean_penetration'][idx_opt],
                    sol['saturation'][idx_opt] * 100,
                    linestyle='--', color=colors[3])[0]

            # Get feasible penetrations
            is_val = sol['capacity'].notnull().all(
                dim=dim_comp_reg_name)
            ipen_rng = np.nonzero(is_val.values)[0][[0, -1]].tolist()

            # Get index before shortage or saturation
            idx_no_shortage = np.nonzero(
                (sol['shortage'] < tau_critic).values)[0].tolist()
            idx_no_saturation = np.nonzero(
                (sol['saturation'] < tau_critic).values)[0].tolist()
            idx_no_critic = np.sort(np.intersect1d(
                np.intersect1d(idx_no_shortage, idx_no_saturation),
                idx_opt))

            # Plot mean-risk
            ax.plot(sol['risk'][idx_opt] * 100,
                    sol['mean_penetration'][idx_opt] * 100,
                    linestyle='--', linewidth=1, color=colors[k], zorder=1)
            # Thicker plot of non critical situations
            if len(idx_no_critic) > 0:
                ax.plot(sol['risk'][idx_no_critic] * 100,
                        sol['mean_penetration'][idx_no_critic] * 100,
                        linestyle='-', linewidth=2, color=colors[k],
                        zorder=1)

            # Get the index of the minimum risk under
            # capacity constraint
            if cap_val:
                mean_penetration = sol['mean_penetration'][
                    idx_min_risk].values * 100
                risk = sol['risk'][idx_min_risk].values * 100
                ratio = mean_penetration / risk
                pv_frac = sol['pv_frac'][idx_min_risk].values
                ax.scatter(risk, mean_penetration,
                           s=msize**2, c=colors[k], marker='o', zorder=2)

                if not cfg_plot.get('no_verbose'):
                    log.info('Minimum risk scenario:')
                    log.info('  Mean total penetration: {:.1f} %'.format(
                        mean_penetration))
                    log.info('  Risk: {:.1f} %'.format(risk))
                    log.info('  Mean-risk ratio: {:.3f}'.format(ratio))
                    log.info('  pv fraction: {:.1f} %'.format(
                        pv_frac * 100))

                # Mark the optimal mix with the same level of risk
                # as the observed mix
                idx_risk_as_obs = np.argmin(
                    np.abs(sol['risk'][idx_min_risk:] - risk_obs))
                pen_risk_as_obs = (
                    sol['mean_penetration'][idx_min_risk:][
                        idx_risk_as_obs]).values * 100
                risk_as_obs = sol['risk'][idx_min_risk:][
                    idx_risk_as_obs].values * 100
                pv_frac_as_obs = sol['pv_frac'][idx_min_risk:][
                    idx_risk_as_obs]
                pv_frac_as_obs = pv_frac_as_obs.values * 100
                if not cfg_plot.get('no_verbose'):
                    log.info('Same risk as the observed mix:')
                    log.info('  Mean total penetration: {:.1f} %'.format(
                        pen_risk_as_obs))
                    log.info('  Risk: {:.1f} %'.format(risk_as_obs))
                    log.info(
                        '  Mean-risk ratio: {:.3f}'.format(
                            pen_risk_as_obs / risk_as_obs))
                    log.info('  pv fraction: {:.1f} %'.format(
                        pv_frac_as_obs))
                if (idx_risk_as_obs + idx_min_risk) < ipen_rng[-1]:
                    ax.scatter(
                        risk_as_obs, pen_risk_as_obs, s=msize**2*1.2,
                        c=colors[k], marker='d', zorder=2)
                    ax_ratio1.vlines(
                        pen_risk_as_obs, ymin=ymin_ratio, ymax=ymax_ratio,
                        linestyle='--', linewidth=1, color=colors[k],
                        zorder=2)

                if not optimal_only:
                    # Mark the non-optimal part
                    ax.plot(
                        sol['risk'][:idx_min_risk] * 100,
                        sol['mean_penetration'][:idx_min_risk]
                        * 100, linestyle='--', linewidth=2, color='0.5',
                        zorder=1)

                # Plot on pv fraction
                ax_ratio1.vlines(
                    [sol['target_mean_penetration'][idx_min_risk]],
                    ymin=ymin_ratio, ymax=ymax_ratio, linestyle='--',
                    linewidth=1, color=colors[k], zorder=2)
            else:
                # Shadow impossible ratios
                x_poly = [xlim[0], sol['risk'][0] * 100,
                          sol['risk'][-1] * 100, xlim[0]]
                y_poly = np.array([
                    sol['mean_penetration'][0],
                    sol['mean_penetration'][0],
                    sol['mean_penetration'][-1],
                    sol['mean_penetration'][-1]]) * 100
                ax.fill(x_poly, y_poly, '0.8')

                # Plot point of agreement
                idx_agree = np.argmin(
                    (sol['capacity'].sum(dim_comp_reg_name)
                     - ref_tot_cap)**2)
                mean_penetration = sol['mean_penetration'][
                    idx_agree].values * 100
                risk = sol['risk'][idx_agree].values * 100
                pv_frac = sol['pv_frac'][idx_agree].values * 100
                ratio = mean_penetration / risk
                ax.scatter(risk, mean_penetration,
                           s=msize**2, c=colors[k], marker='o', zorder=2)

                if not cfg_plot.get('no_verbose'):
                    log.info('Maximum ratio scenario:')
                    log.info('  Mean total penetration: {:.1f} %'.format(
                        mean_penetration))
                    log.info('  Risk: {:.1f} %'.format(risk))
                    log.info('  Mean-risk ratio: {:.3f}'.format(ratio))
                    log.info('  pv fraction: {:.1f} %'.format(pv_frac))

                # Plot on pv fraction
                ax_ratio1.vlines(
                    [sol['target_mean_penetration'][idx_agree]],
                    ymin=ymin_ratio, ymax=ymax_ratio, linestyle='--',
                    linewidth=1, color=colors[k], zorder=2)

            # # Plot highest penetration before critical situation occurence
            # if idx_no_critic[0] > ipen_rng[0]:
            #     ax.scatter(
            #         (sol['risk'] * 100)[idx_no_critic[0]],
            #         (sol['mean_penetration'] * 100)[idx_no_critic[0]],
            #         s=msize**2, c=colors[k], marker='D', zorder=2)
            # if idx_no_critic[-1] < ipen_rng[-1]:
            #     ax.scatter((sol['risk'] * 100)[idx_no_critic[-1]],
            #                (sol['mean_penetration'] *
            #                 100)[idx_no_critic[-1]],
            #                s=msize**2, c=colors[k], marker='D', zorder=2)

            # Plot feasibility limit
            if (not optimal_only) & (ipen_rng[0] > 0):
                ax.scatter((sol['risk'] * 100)[ipen_rng[0]],
                           (sol['mean_penetration'] * 100)[ipen_rng[0]],
                           s=msize**2, c=colors[k], marker='s', zorder=2)
            if (ipen_rng[-1] <
                    sol.dims['target_mean_penetration'] - 1):
                ax.scatter(
                    (sol['risk'] * 100)[ipen_rng[-1]],
                    (sol['mean_penetration'] * 100)[ipen_rng[-1]],
                    s=msize**2, c=colors[k], marker='s', zorder=2)

        # Plot techno and none cases if possible
        cap_val = False
        ls = ['--', '-.']
        for ist, strategy in enumerate(['techno', 'none']):
            case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
            if case_name in self:
                sol = self[case_name]
                if not cfg_plot.get('no_verbose'):
                    mean_penetration = sol['mean_penetration'][
                        idx_agree].values * 100
                    risk = sol['risk'][idx_agree].values * 100
                    pv_frac = sol['pv_frac'][idx_agree].values * 100
                    ratio = mean_penetration / risk
                    log.info('{} mix:'.format(strategy))
                    log.info('Maximum ratio scenario:')
                    log.info('  Mean total penetration: {:.1f} %'.format(
                        mean_penetration))
                    log.info('  Risk: {:.1f} %'.format(risk))
                    log.info('  Mean-risk ratio: {:.3f}'.format(ratio))
                    log.info('  pv fraction: {:.1f} %'.format(pv_frac))
                ax.plot(sol['risk'] * 100, sol['mean_penetration'] * 100,
                        linestyle=ls[ist], linewidth=1, color=colors[0],
                        zorder=3)

        # Get result postfix
        _, comm1, _ = np.intersect1d(
            *result_postfixes, return_indices=True)
        result_postfix = '_'.join(result_postfixes[0][np.sort(comm1)])

        ax.set_xlim(xlim)
        # Adjust both y-axis limits so that both curves ends match
        if optimal_only:
            ylim = (15., 23.)
        else:
            ylim = (sol['target_mean_penetration'][0],
                    sol['target_mean_penetration'][-1])
        ax.set_ylim(ylim)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax.set_xlabel('Risk (%)', fontsize=cfg_plot['fs_default'])
        ax.set_ylabel('Mean (%)', color=colors[0],
                      fontsize=cfg_plot['fs_default'])

        # Save fronts figure
        fig_filename = 'front{}.{}'.format(result_postfix, fig_format)
        fig_filepath = os.path.join(front_dir, fig_filename)
        if not cfg_plot.get('no_verbose'):
            log.info('Saving front figure to {}'.format(fig_filepath))
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        # Configure and save pv fraction
        plt.legend([h_ratio, h_short, h_sat],
                   ['pv fraction', 'Shortage', 'Saturation'], loc='best')
        ax_ratio1.set_xlabel('Mean (%)',
                             fontsize=cfg_plot['fs_default'])
        ax_ratio1.set_ylabel('pv (%)', color=colors[2],
                             fontsize=cfg_plot['fs_default'])
        ax_ratio2.set_ylabel('Shortage and Saturation (%)', color=colors[3],
                             fontsize=cfg_plot['fs_default'])
        ax_ratio1.set_xlim(ylim)
        ax_ratio1.set_ylim(ymin_ratio, ymax_ratio)
        ax_ratio2.set_ylim(0., 12.)
        ax_ratio1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_ratio1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        ax_ratio2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        # Save fronts figure
        fig_filename = 'pv_frac{}.{}'.format(result_postfix, fig_format)
        fig_filepath = os.path.join(pv_frac_dir, fig_filename)
        if not cfg_plot.get('no_verbose'):
            log.info('Saving pv fraction figure to {}'.format(fig_filepath))
        fig_ratio.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)

    def plot_capacity(self, strategy='global', **kwargs):
        """Plot map of regional capacity from solution.

        :param strategy: Strategy (`'global'`, `'techno'`, or `'none'`)
        :type strategy: str
        """
        dim_comp_reg_name = 'component_region'
        dim_comp_reg = {dim_comp_reg_name: ('component', 'region_multi')}
        cfg_plot = load_config(self.med.cfg, 'plot')
        fig_format = cfg_plot['savefigs_kwargs']['format']
        map_dir = self.med.cfg.get_plot_directory(
            self.opt, subdirs='map', **kwargs)

        # Make sure input data is loaded
        self.opt.input.get_data(**kwargs)
        pv_loc = self.opt.input['cf'].component == 'pv'
        wind_loc = self.opt.input['cf'].component == 'wind'

        # Select constrained solution
        cap_val = True
        case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
        sol = self[case_name]

        # Select unconstrained solution
        cap_val = False
        case_name = 'strategy{}tot_cap{}'.format(strategy, str(cap_val))
        sol_free = self[case_name]

        # Read the regions coordinates and ensure order
        self.med.geo_src.get_data()
        df_coords = self.med.geo_src.read_region_coordinates(**kwargs)
        df_coords = df_coords.loc[sol['region'], :]
        lat, lon = df_coords['lat'].values, df_coords['lon'].values

        # Get total capacity
        capa_ref, _ = self.opt.get_reference_capacity(**kwargs)
        ref_tot_cap = self.opt.get_reference_total_capacity(
            capa_ref, **kwargs)

        # Make sure regions coordinates are ordered
        idx_agree = np.argmin(
            (sol_free.capacity.sum(dim_comp_reg_name)
             - ref_tot_cap)**2)
        target_mean_pen = float(sol['target_mean_penetration'][idx_agree])
        risk = float(sol['risk'][idx_agree])
        mean_penetration = float(sol['mean_penetration'][idx_agree])
        # Plot maximum ratio map
        if not cfg_plot.get('no_verbose'):
            log.info('Plotting for the maximum ratio at penetration '
                     '{:.1f}% and risk {:.1f}%'.format(
                         mean_penetration * 100, risk * 100))
        capa_pv = sol['capacity'][{'target_mean_penetration': idx_agree,
                                   dim_comp_reg_name: pv_loc}]
        capa_wind = sol['capacity'][{'target_mean_penetration': idx_agree,
                                     dim_comp_reg_name: wind_loc}]
        starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
        result_postfix = '{}_{}'.format(self.get_data_postfix(),
                                        strategy)
        fig_filename = 'map_capacity{}{}.{}'.format(
            result_postfix, starget, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                            mean_penetration=mean_penetration, **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        idx_min_risk = int(np.argmin(sol['risk']))
        target_mean_pen = float(sol['target_mean_penetration'][
            idx_min_risk])
        risk = float(sol['risk'][idx_min_risk])
        mean_penetration = float(sol['mean_penetration'][idx_min_risk])
        capa_pv = sol['capacity'][{'target_mean_penetration': idx_min_risk,
                                   dim_comp_reg_name: pv_loc}]
        capa_wind = sol['capacity'][{
            'target_mean_penetration': idx_min_risk,
            dim_comp_reg_name: wind_loc}]
        if not cfg_plot.get('no_verbose'):
            log.info('Plotting at penetration {:.1f}% for the minimum risk '
                     '{:.1f}%'.format(mean_penetration * 100, risk * 100))
        starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
        fig_filename = 'map_capacity{}{}.{}'.format(
            result_postfix, starget, fig_format)
        fig_filepath = os.path.join(map_dir, fig_filename)
        fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                            mean_penetration=mean_penetration, **kwargs)
        fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        # Add observed mean/risk point of the observed mix
        dem_tot_mean = float(self.opt.input['dem_mean'].sum('region'))

        # Define the risk function
        # Objective function and its arguments
        args0 = (self.opt.input['cf_cov'].values,)
        fun0 = fun_var
        x = capa_ref.rename({'region': 'region_multi'}).stack(
            **dim_comp_reg)

        # Get the mean penetration and the risk of the observed mix
        risk_obs = np.sqrt(fun0(x, *args0)) / dem_tot_mean

        # Plot for increased penetration for the same decrease of
        # mean/risk ratio
        # idx_max_mean = int(np.argmax(sol['mean_penetration']))
        is_val = sol['capacity'].notnull().all(dim=dim_comp_reg_name)
        itarget_mean_pen_rng = np.nonzero(
            is_val.values)[0][[0, -1]].tolist()
        idx_risk_as_obs = np.argmin(
            np.abs(sol['risk'][idx_min_risk:] - risk_obs))
        if (idx_risk_as_obs + idx_min_risk) < itarget_mean_pen_rng[-1]:
            target_mean_pen = float(sol['mean_penetration'][idx_min_risk:][
                idx_risk_as_obs].values * 100)
            risk = float(sol['risk'][idx_min_risk:]
                         [idx_risk_as_obs].values)
            mean_penetration = float(sol['mean_penetration'][idx_min_risk:]
                                     [idx_risk_as_obs].values)
            idx = np.arange(len(sol['risk']))[idx_min_risk:][
                idx_risk_as_obs]
            capa_pv = sol['capacity'][{'target_mean_penetration': idx,
                                       dim_comp_reg_name: pv_loc}]
            capa_wind = sol['capacity'][{
                'target_mean_penetration': idx,
                dim_comp_reg_name: wind_loc}]
            if not self.cfg.get('no_verbose'):
                log.info('Plotting at penetration {:.1f}% for a risk '
                         '{:.1f}% identical to that of the observed '
                         'mix'.format(mean_penetration * 100, risk * 100))
            starget = '_avgpen_{}'.format(int(target_mean_pen * 100 + 0.1))
            fig_filename = 'map_capacity{}{}.{}'.format(
                result_postfix, starget, fig_format)
            fig_filepath = os.path.join(map_dir, fig_filename)
            fig = plot_geo_dist(self, lat, lon, capa_pv, capa_wind,
                                mean_penetration=mean_penetration, **kwargs)
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

        if cfg_plot['show']:
            plt.show(block=False)


def fun_collector(functions, weights=None, collector=sum):
    """Define a new function `f(x, *args)` given by some (weighted)
    aggregation of given functions (e.g. weighted sum).
    Each function `functions[k](x, *args[k])`
    takes the same first argument `x`, as secondary arguments
    those in the sequence `args[k]`, and returns a scalar.

    :param functions: Functions to aggregate.
    :param weights: Weights assigned to each summed function.
      If None, all functions are given the same weight one.
      Default is `None`.
    :param collector: Function used to aggregate the results
      of the given sequence of functions. Default is :py:func:`sum`.
    :type functions: sequence
    :type weights: sequence
    :type collector: function

    :returns: Function taking as arguments `x` and a sequence of sequences
      of other arguments of all functions,
      in the same order as :py:obj:`functions`, and returning the weighted sum
      of results of functions as a float.
    :rtype: function
    """
    # Use uniform weights if not given
    if weights is None:
        weights = [1.] * len(functions)

    # Define collector
    def f(x, args):
        return collector([(weights[k] * functions[k](x, *(args[k])))
                          for k in range(len(functions))])

    return f


def fun_var(x, cf_cov, **kwargs):
    """Objective function given by the variance associated with
    a capacity distribution and a capacity factors covariance matrix.

    :param x: State vector.
    :param cf_cov: pv/wind capacity factors covariances.
    :type x: :py:class:`numpy.array`
    :type cf_cov: :py:class:`numpy.array`

    :returns: Value of objective function.
    :rtype: float
    """
    # Compute objective
    obj = np.dot(x, np.dot(cf_cov, x))

    return obj


def jac_var(x, cf_cov, **kwargs):
    """Jacobian of objective function given by the variance associated with
    a capacity distribution and a capacity factors covariance matrix.

    :param x: State vector.
    :param cf_cov: pv/wind capacity factors covariances.
    :type x: :py:class:`numpy.array`
    :type cf_cov: :py:class:`numpy.array`

    :returns: Value of objective function.
    :rtype: float
    """
    # Compute objective
    jac = 2 * np.dot(cf_cov, x)

    return jac


def mean_risk_ratio(ds, **kwargs):
    """Analytically compute optimal Mean/Risk ratio

    .. math::
      \frac{\mu(w^*)}{\sqrt{\sigma^2(w^*)}} = \sqrt{u^t \Sigma^{-1} u}

    for the unconstrained electricity mix optimization problem.

    :param ds: Dataset collecting the inputs for optimization problem.
    :type ds: :py:obj:`xarray.Dataset`
    """
    inv_cf_cov = np.linalg.inv(ds['cf_cov'])
    mean_risk_ratio = np.dot(ds['cf_mean'], np.dot(
        inv_cf_cov, ds['cf_mean']))

    return np.sqrt(mean_risk_ratio)


def fun_total_penetration(x, pen_reg, target_mean_pen):
    """Function defining the equality constraint on total target penetration.

    :param x: State vector.
    :param pen_reg: Penetration rates for each region and component.
    :param target_mean_pen: Total target penetration.
    :type x: :py:class:`numpy.array`
    :type pen_reg: :py:class:`numpy.array`
    :type target_mean_pen: float

    :returns: Value of the left-hand side of constraint.
    :rtype: float
    """
    return target_mean_pen - np.dot(pen_reg, x)


def jac_total_penetration(x, pen_reg, *args):
    """Function defining Jacobian of the equality constraint
    on total target penetration.

    :param x: State vector(not used).
    :param pen_reg: Penetration rates for each region and component.
    :type x: :py:class:`numpy.array`
    :type pen_reg: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -pen_reg


def fun_tot_cap(x, tot_cap):
    """Function defining the equality constraint on total capacity.

    :param x: State vector.
    :param tot_cap: Total capacity.
    :type x: :py:class:`numpy.array`
    :type tot_cap: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    return tot_cap - x.sum()


def jac_tot_cap(x, *args):
    """Function defining Jacobian of equality constraint on total capacity.

    :param x: State vector.
    :type x: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -np.ones((x.shape[0],))


def fun_tot_cap_squared(x, tot_cap):
    """Function defining soft equality constraint on total capacity
    by returning squared deviation from total capacity.

    :param x: State vector.
    :param tot_cap: Total capacity.
    :type x: :py:class:`numpy.array`
    :type tot_cap: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    return (tot_cap - x.sum())**2


def jac_tot_cap_squared(x, tot_cap):
    """Function defining Jacobian of soft equality constraint
    on total capacity.

    :param x: State vector.
    :type x: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -2 * np.ones((x.shape[0],)) * (tot_cap - x.sum())


def fun_regional_transmission(x, *args):
    """Function defining inequality constraint on regional transmission.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param trans: Regional transimission capacity.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type trans: :py:class:`numpy.array`

    :returns: Value of left-hand side of constraint.
    :rtype: :py:class:`numpy.array`
    """
    dem_t = args[1]
    nt, n_reg = dem_t.shape
    trans_t = np.tile(args[2], (nt, 1))
    omega_t = np.tile(x, (nt, 1))
    omega_t_pv = omega_t[:, :n_reg]
    omega_t_wind = omega_t[:, n_reg:]
    cf_t_pv = args[0][:, :n_reg]
    cf_t_wind = args[0][:, n_reg:]
    #  :math:`T_i+D_i(t)-\omega_i \eta_i(t)-\omega_{i + n_reg}
    #      \eta_{i + n_reg}(t)`
    y = (trans_t + dem_t - omega_t_pv * cf_t_pv -
         omega_t_wind * cf_t_wind).flatten()

    return y


def jac_regional_transmission(x, *args):
    """Function defining Jacobian of inequality constraint
    on regional transimission.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param trans: Regional transimission capacity.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type trans: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    dem_t = args[1]
    nt, n_reg = dem_t.shape
    cf_t = args[0]
    cf_t_pv = cf_t[:, :n_reg]
    cf_t_wind = cf_t[:, n_reg:]
    jac = np.zeros((n_reg * 2, nt * n_reg))
    for k in np.arange(n_reg):
        jac[k, k::n_reg] = -cf_t_pv[:, k]
        jac[k + n_reg, k::n_reg] = -cf_t_wind[:, k]

    # Return transpose of Jacobian as scipy stacks constraints vertically
    return jac.T


def fun_shortage(x, cf, dem, max_conventional):
    """Function defining inequality constraint on RES production shortage,
    when the production from RES is not able
    to meet fraction of demand not met by conventional components.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_conventional: Maximum possible total conventional production.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_conventional: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    nt, n_reg = dem.shape
    omega_t = np.tile(x, (nt, 1))

    y = (omega_t * cf).sum(1) + max_conventional - dem.sum(1)

    return y


def jac_shortage(x, cf, *args):
    """Function defining Jacobian of inequality constraint on
    RES production shortage, when production from RES is not able
    to meet fraction of demand not met by conventional components.

    :param x: State vector(not used).
    :param cf: Time-dependent capacity factors.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return cf


def shortage_frequency(x, *args):
    """Compute frequency of occurence of shortage situations
    defined as situations when the production from RES is not able
    to meet the fraction of the demand not met by conventional components.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_conventional: Maximum possible total conventional production.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_conventional: float

    :returns: Frequency of occurence of shortage situations.
    :rtype: float
    """
    y = fun_shortage(x, *args)
    y_val = y[~np.isnan(y)]
    shortage_frequency = np.sum(y_val < 0.) / y_val.shape[0]

    return shortage_frequency


def fun_saturation(x, cf, dem, max_res):
    """Function defining the inequality constraint on the saturation,
    defined as situations when the production from RES exceeds
    the theoretical limit that the network can support.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_res: Maximum RES penetration, i.e. maximum fraction
      of production from RES over demand that the network can support.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_res: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    nt, n_reg = dem.shape
    omega_t = np.tile(x, (nt, 1))

    y = max_res * dem.sum(1) - (omega_t * cf).sum(1)

    return y


def jac_saturation(x, cf, *args):
    """Function defining Jacobian of the inequality constraint
    on the saturation, defined as situations when the production from RES
    exceeds the theoretical limit that the network can support.

    :param x: State vector(not used).
    :param cf: Time-dependent capacity factors.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`

    :returns: Value of Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    return -cf


def saturation_frequency(x, cf, dem, max_res):
    """Compute frequency of occurence of saturation situations
    defined as situations when the production from RES exceeds
    the theoretical limit that the network can support.

    :param x: State vector.
    :param cf: Time-dependent capacity factors.
    :param dem: Time-dependent regional demand.
    :param max_res: Maximum RES penetration, i.e. the maximum
        fraction of production from RES over the demand that the network
        can support.
    :type x: :py:class:`numpy.array`
    :type cf: :py:class:`numpy.array`
    :type dem: :py:class:`numpy.array`
    :type max_res: float

    :returns: Frequency of occurence of saturation situations.
    :rtype: float
    """
    y = fun_saturation(x, cf, dem, max_res)
    y_val = y[~np.isnan(y)]
    saturation_frequency = np.sum(y_val < 0.) / y_val.shape[0]

    return saturation_frequency


def fun_profit(x, cf_mean, capex, opex, elec_price, n_years, profit_target):
    """Constraint associated with profit from electricity production sell.

    :param x: State vector(power).
    :param cf_mean: Mean capacity factors.
    :param capex: CAPital EXpenditure (currency/power).
    :param opex: OPeration EXpenditure (currency/power/yr).
    :param elec_price: Electricity selling price (currency/power/h).
    :param n_years: Number of years of excercise.
    :param profit_target: Target profit.
    :type x: :py:class:`numpy.array`
    :type cf_mean: :py:class:`numpy.array`
    :type capex: float
    :type opex: float
    :type elec_price: float
    :type n_years: float
    :type profit_target: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    hour2_year = 24 * 365

    # Profit from selling electricity
    profit = np.sum(x * (hour2_year * n_years * cf_mean * elec_price
                         - (capex + n_years * opex))) / n_years

    # Profit at least target profit
    y = profit - profit_target

    return y


def jac_profit(x, cf_mean, capex, opex, elec_price, n_years, *args):
    """Jacobian of constraint associated with profit from
    electricity production sell.

    :param x: State vector(power, not used).
    :param cf_mean: Mean capacity factors.
    :param capex: CAPital EXpenditure (currency/power).
    :param opex: OPeration EXpenditure (currency/power/yr).
    :param elec_price: Electricity selling price (currency/power/h).
    :param n_years: Number of years of excercise.
    :type x: :py:class:`numpy.array`
    :type cf_mean: :py:class:`numpy.array`
    :type capex: float
    :type opex: float
    :type elec_price: float
    :type n_years: float

    :returns: Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    hour2_year = 24 * 365

    jac = (hour2_year * n_years * cf_mean * elec_price
           - (capex + n_years * opex)) / n_years

    return jac


def fun_pv_frac(x, pv_loc, pv_frac):
    """Function defining equality constraint on fraction of pv capacity
    over pv + wind capacity.

    :param x: State vector.
    :param pv_loc: Boolean index of pv capacities.
    :param pv_frac: pv capacity over total capacity.
    :type x: :py:class:`numpy.array`
    :type pv_loc: :py:class:`numpy.array`
    :type pv_frac: float

    :returns: Value of left-hand side of constraint.
    :rtype: float
    """
    jac = -np.ones((x.shape[0],)) * pv_frac
    jac[pv_loc] += 1.

    y = np.dot(jac, x)

    return y


def jac_pv_frac(x, *args):
    """Jacobian of function defining equality constraint
    on fraction of pv capacity over pv + wind capacity.

    :param x: State vector.
    :param pv_frac: pv capacity over total capacity (pv + wind).
    :type x: :py:class:`numpy.array`
    :type pv_frac: float

    :returns: Jacobian of constraint.
    :rtype: :py:class:`numpy.array`
    """
    n_reg = int((x.shape[0] + 0.1) / 2)
    pv_frac = args[0]
    jac = -np.ones((x.shape[0],)) * pv_frac
    jac[:n_reg] += 1.

    return jac


def get_bounds_cstr(lb=None, ub=None, dim=None, sparse=False):
    """Get linear constraint corresponding to lower and upper bounds
    on state.

    :param lb: Lower bound(s). Default is `None`.
    :param ub: Upper bound(s). Default is `None`.
    :param dim: Problem dimension. Should be given if bounds are scalar.
      Default is `None`.
    :param sparse: If `True`, return matrices as spmatrix
        and vectors as matrix. Default is `False`.
    :type lb: float, :py:class:`numpy.array`
    :type ub: float, :py:class:`numpy.array`
    :type dim: int
    :type sparse: bool

    :returns: A tuple containing matrix :math:`G` and vector
         :math:`h` defining constraint :math:`G x \le h`.
    :rtype: tuple of :py:class:`numpy.array`,
        or :py:obj:`cvxspmatrix` and :py:obj:`cvxmatrix`.

    .. note:: Constraint is adapted to the quadprod module.
        To use the CVXOPT module, the oposite should be taken.
    """
    # Make sure that bounds are vectors
    h = []
    G, v, i, j = [], [], [], []
    if lb is not None:
        if not hasattr(lb, "__len__"):
            lba = np.ones((dim,)) * lb
        else:
            dim = len(lb)
            lba = lb
        if sparse:
            v.append(-1. * np.ones(dim))
            i.append(np.arange(dim))
            j.append(np.arange(dim))
        else:
            G.append(-np.eye(dim))
        h.append(-lba)
    if ub is not None:
        if not hasattr(ub, "__len__"):
            uba = np.ones((dim,)) * ub
        else:
            dim = len(ub)
            uba = ub
        if sparse:
            v.append(np.ones(dim))
            i.append(np.arange(dim))
            j.append(np.arange(dim))
        else:
            G.append(np.eye(dim))
        h.append(uba)

    # Matrix G and vector h for  :math:`G x \le h`
    h = np.concatenate(h)
    if sparse:
        v = np.concatenate(v)
        i = np.concatenate(i)
        j = np.concatenate(j)
        G = spmatrix(v, i, j)
        h = matrix(h)
    else:
        G = np.concatenate(G, axis=0)

    return (G, h)


def get_weighted_sum_cstr(weights, target_sum):
    """Get linear equality constraint corresponding
    to a weighted sum.

    :param weights: Weights of mean.
    :param target_sum: Target value of weighted sum.
    :type weights: :py:class:`numpy.array`
    :type target_sum: float

    :returns: A tuple containing matrix :math:`A` and vector
         :math:`b` defining constraint :math:`A x = b`.
    :rtype: tuple of :py:class:`numpy.array`.
    """
    return (np.expand_dims(weights, 0), np.array([target_sum]))


def fun_distribute_cv_square(x, *args):
    """Objective function on conventional power and transmission for
    power flow analysis.

    :param x: Conventional power at each node.
    :param power_mismatch: Difference between load and the production
      at each node (MW).
    :param q: Parameter controling the weight given to minimization
      of conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :type power_mismatch: :py:class:`numpy.array`
    :type q: float

    :returns: Value of objective function.
    :rtype: float
    """
    power_mismatch, q = args

    obj = ((1. - q) * np.sum(x**2) + q * np.sum((x - power_mismatch)**2))

    return obj


def jac_distribute_cv_square(x, *args):
    """Jacobian of objective function on conventional power
    and transmission for power flow analysis.

    :param x: Conventional power at each node.
    :param power_mismatch: Difference between load and production
      at each node (MW).
    :param q: Parameter controling the weight given to minimization
      of conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :type power_mismatch: :py:class:`numpy.array`
    :type q: float

    :returns: Jacobian vector of objective function.
    :rtype: :py:class:`numpy.array`
    """
    power_mismatch, q = args

    jac = 2 * (x - q * power_mismatch)

    return jac


def distribute_cv_square(power_mismatch, r):
    """Distribute conventional capacity optimally while supplying mismatch
    between load and fatal production at each time step,
    independently of other types of production.

    :param power_mismatch: Difference between load and RES production
      at each node(MW).
    :param r: Parameter controling weight given to minimization of
      conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :type power_mismatch: :py:class:`numpy.array`
    :type r: float

    :returns: Conventional production at each node.
    :rtype: :py:class:`numpy.array`

    .. note::
        * The conventional production is optimally distributed subject
            to the total production summing to zero at each time step,
            i.e. such that the sum of the conventional and the RES production
            equals the load, constraining the conventional production at
            all nodes but the first one to be positive.
            Without this bound, one would have:

                * For :math:`r = 0`, the conventional production is uniformly
                    distributed.
                * For :math:`r = 1`, the conventional production compensates
                    the mismatch between the RES produciton and the demand,
                    i.e. there is no transmission.
                * For :math:`0 \le r \le 1`, the conventional production is given by

            .. math::
                (1 - r) \sum_{i = 1} ^ N \frac{P ^ {\mathrm{_res}}_i - dem_i}{N}
                - r(P ^ {\mathrm{_res}}_i - dem_i)

        * Since may(for each time step) small
            (the size given by the number of regions)
            quadratic programming problems, we use the active region
            quadratic programming algorithm implemented in quadprog.
    """
    nt, n_reg = power_mismatch.shape

    # Get matrix defining quadratic objective function
    P = 2 * np.eye(n_reg)

    # Get matrix and vector defining positiveness constraints
    # on CV production
    lb = np.zeros((n_reg,))
    # Allow for negative production on slack bus 1
    lb[0] = -1.e27
    (G0, h0) = get_bounds_cstr(lb=lb, dim=n_reg)
    G0, h0 = -G0, -h0

    # Solve problem at each time step
    P_cv = np.empty((nt, n_reg))
    for t in np.arange(nt):
        Pt = power_mismatch[t]

        # Get vector defining quadratic objective function
        q = -2 * r * Pt

        # Get matrix and vector defining constraint on sum of
        # conventional capacity supplying mismatch
        (A, b) = get_weighted_sum_cstr(np.ones((n_reg,)), Pt.sum())

        # Concatenate equality and inequality constraints
        G = np.concatenate([A, G0], axis=0)
        h = np.concatenate([b, h0], axis=0)

        # Optimize
        res = solve_qp(P, -q, G.T, h, meq=1)

        # Save result
        P_cv[t] = res[0]

    return P_cv


def distribute_cv_mean_square(power_mismatch, r, window_length=None):
    """Distribute conventional capacity while supplying mismatch between
    load and production, minimizing variance.

    :param power_mismatch: Difference between load and production
      at each node (MW).
    :param r: Parameter controling weight given to minimization of
      conventional production versus minmization of transmission.
      Set to `0` to minimize conventional production alone.
      Set to `1` to minimize transmission alone.
    :param window_length: Length of windows over which to average.
        If `None`, average over whole time series. Default is `None`.
    :type power_mismatch: :py:class:`numpy.array`
    :type r: float
    :type window_length: int

    :returns: Conventional production at each node.
    :rtype: :py:class:`numpy.array`

    .. note::

        * The conventional production is optimally distributed subject
          to the total production summing to zero at each time step,
          i.e. such that the sum of the conventional and the RES production
          equals the load, while constraining the conventional production
          at all nodes but the first one to be positive.
          The optimization is done with a compromise between
          the variance of the conventional production(q close to 0) and the
          variance of the transmission(q close to 1).
        * The optimization problem being high dimensional, due to the states
          including several time steps and all regions,
          we use the interio-point quadratic programming algorithm.

    """
    nt, n_reg = power_mismatch.shape
    if window_length is None:
        window_length = nt
    n_window = int(nt / window_length)
    rest = np.mod(nt, window_length)
    if rest > 0:
        # If remaining is long, add a window, otherwise keep in previous window
        if rest > window_length / 2:
            n_window += 1

    # Configure solver
    solvers.options['show_progress'] = False

    # Loop over windows
    P_cv = np.empty((nt, n_reg))
    for window in np.arange(n_window):
        # Get mismatch power window, making sure to cover whole time series
        if window == (n_window - 1):
            Pm_window = power_mismatch[window*window_length:]
        else:
            Pm_window = power_mismatch[window *
                                       window_length:(window+1)*window_length]

        # Last window may be shorter, update length
        nt_window = Pm_window.shape[0]
        dim = n_reg * nt_window

        # Get matrix defining quadratic objective function
        P = spmatrix(2. / nt_window, np.arange(dim), np.arange(dim))

        # Get matrix and vector defining positiveness constraints
        # on CV production
        lb = np.zeros((dim,))
        # Allow for negative production on slack bus 1
        lb[:nt_window] = -1.e15
        (G, h) = get_bounds_cstr(lb=lb, sparse=True)

        # Get matrix and vector defining constraint on sum of
        # conventional capacity supplying mismatch
        A = np.zeros((nt_window, dim))
        v = np.ones((dim,))
        i = np.tile(np.arange(nt_window), n_reg)
        j = np.arange(dim)
        A = spmatrix(v, i, j)
        b = matrix(Pm_window.sum(1))

        # Get vector defining quadratic objective function
        q = -r * P * matrix(Pm_window.T.flatten())

        # Use previous optimum as initial state if possible
        if (window > 0):
            # Make sure that vectors have same length
            if len(res['y']) == nt_window:
                initvals = {'x': res['x'], 's': res['s'], 'y': res['y'],
                            'z': res['z']}
            else:
                initvals = None

        else:
            initvals = None

        # Optimize
        res = solvers.qp(P, q, G=G, h=h, A=A, b=b, initvals=initvals)

        # Save result
        x = np.array(res['x'])[:, 0].reshape(n_reg, nt_window).T
        if window == (n_window - 1):
            P_cv[window*window_length:] = x
        else:
            P_cv[window*window_length:(window+1)*window_length] = x

    return P_cv


def quad_prog_active_set(G, c, A, b=None):
    """Brute-force active set method to solve convex quadratic program

    .. math::

         \min_x x^t G x + c^t x

         \mathrm{subject~to~} A^t x >= b.

    :param G: Positive definite matrix.
    :param c: Linear vector.
    :param A: Linear constraint matrix.
    :param b: Constant vector for linear constraints.
    :type G: array_like
    :type c: array_like
    :type A: array_like
    :type b: array_like

    :returns: Tuple containing:

        * Optimization problem solution.
        * Lagrange multipliers.

    :rtype: tuple of :py:class:`~numpy.array`

    .. note:: This function is used for pedagogical purposes only.
      Favor using more advanced solvers (e.g. quadprog or from scipy).
    """
    m, n = A.shape
    idx = np.arange(n)
    b = np.zeros((m,)) if b is None else b

    # Inverse covariance matrix
    Gm1 = np.linalg.inv(G)

    # Get initial guess solving unbounded problem
    x = -Gm1.dot(c)

    # Get active set
    ix0 = x < 0
    W = ix0.nonzero()[0]
    x[ix0] = 0.
    while True:
        log.info('Active set:', W)
        m = W.shape[0]
        # Solve for step and Lagrange multipliers
        K = np.zeros((n + m, n + m))
        K[:n, :n] = G
        K[n:, :n] = A[W]
        K[:n, n:] = -A[W].T
        g = G.dot(x) + c
        pl = np.linalg.inv(K).dot(np.concatenate([-g, np.zeros((m,))]))
        p, lambdak = np.split(pl, [n])

        if np.linalg.norm(p, np.inf) < 1.e-6:
            if (lambdak >= 0).all():
                return x, lambdak
            else:
                # Remove constraint with minimum Lagrangian from active set
                jj = np.argmin(lambdak)
                W = np.setdiff1d(W, jj)
        else:
            # Compute alpha
            Ap = A.dot(p)
            ineg = Ap < 0
            v = np.zeros((n,))
            v[ineg] = (b - A.dot(x))[ineg] / Ap[ineg]
            alpha, iBlock = 1, None
            isel = np.intersect1d(np.setdiff1d(idx, W), ineg.nonzero()[0])
            if len(isel) > 0:
                ivmin = np.argmin(v[isel])
                if v[ivmin] < 1:
                    iBlock, alpha = isel[ivmin], v[isel][ivmin]

            # Update state
            x += alpha * p

            # Add blocking constraint
            W = W if iBlock is None else np.union1d(W, iBlock)


def _save_dict(di, ds, prefix=''):
    """Save a(multi-level) dictionary to a dataset's attributes.

    :param di: Dictionary to save.
      Multi-level dictionaries are flattened and child keys are prefixed
      by parent key.
    :param ds: Dataset in which to save dictionary.
    :param prefix: Prefix to append to child keys of dictionary.
    :type di: dict
    :type ds: :py:class:`xarray.Dataset`
    :type prefix: str
    """
    for key, value in di.items():
        if value is None:
            continue
        elif isinstance(value, bool):
            value = int(value)
        elif isinstance(value, dict):
            _save_dict(value, ds, prefix=(key + '_'))
        else:
            ds.attrs[prefix + key] = value


# def fun_covariance(x, *args):
#     """Objective function given by total covariance.

#     :param x: State vector.
#     :param sigma: Covariance matrix.
#     :type x: :py:class:`numpy.array`
#     :type sigma: :py:class:`numpy.array`

#     :returns: Value of objective function.
#     :rtype: float
#     """
#     obj = np.dot(x, np.dot(args[0], x))

#     return obj


# def jac_covariance(x, *args):
#     """Jacobian of objective function given by total covariance.

#     :param x: State vector.
#     :param sigma: Covariance matrix.
#     :type x: :py:class:`numpy.array`
#     :type sigma: :py:class:`numpy.array`

#     :returns: Jacobian vector.
#     :rtype: :py:class:`numpy.array`
#     """
#     J = 2 * np.dot(args[0], x)

#     return J


# def hess_covariance(x, *args):
#     """Hessian of objective function given by total covariance.

#     :param x: State vector.
#     :param sigma: Covariance matrix.
#     :type x: :py:class:`numpy.array`
#     :type sigma: :py:class:`numpy.array`

#     :returns: Value of Hessian.
#     :rtype: :py:class:`numpy.array`
#     """
#     H = 2 * args[0]

#     return H
