"""Various plot functions."""
import os
import logging
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from .geo import GEO_VARIABLE
from .config import load_config

#: Logger.
log = logging.getLogger(__name__)

#: Default plot-colors.
COLORS = rcParams['axes.prop_cycle'].by_key()['color']


def plot_mask(data_src, crs=None, facecolor='moccasin', edgecolor='dimgrey',
              **kwargs):
    """ Plot the mask assigning climate grid points to regions.

    :param data_src: Data source.
    :param crs: Coordinate Reference System. Default is
      :py:class:`cartopy.crs.LambertAzimuthalEqualArea`.
    :param facecolor: Face color of the regions. Default is `'moccasin'`.
    :param edgecolor: Edge color of the regions. Default is `'dimgrey'`.
    :type data_src: :py:class:`.data_source.DataSourceBase`
    :type crs: :py:class:`cartopy.crs.ABCMeta`
    :type facecolor: str
    :type edgecolor: str
    """
    # Configuration
    med = data_src.med
    cfg_plot = load_config(med.cfg, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    fig_dir = med.cfg.get_plot_directory(data_src, **kwargs)
    markersize = 5
    facecolor = facecolor or cfg_plot.get('region_facecolor') or 'moccasin'
    edgecolor = edgecolor or cfg_plot.get('region_edgecolor') or 'dimgrey'
    crs = crs or ccrs.LambertAzimuthalEqualArea()

    # Get mask
    data_src.get_mask(**kwargs)
    mask = data_src.mask

    # Convert geometry to CRS
    med.geo_src.get_data()
    gdf_crs = med.geo_src.get(GEO_VARIABLE).to_crs(crs.proj4_init)

    # Plot
    if not cfg_plot.get('no_verbose'):
        log.info('Plotting {} mask for {}'.format(
            med.geo_src.name, data_src.name))
    fig = plt.figure()
    ax = plt.axes(projection=crs)
    ax.set_xlabel('Longitude', fontsize=cfg_plot['fs_default'])
    ax.set_ylabel('Latitude', fontsize=cfg_plot['fs_default'])

    # Plot regions
    gdf_crs.plot(ax=ax, facecolor=facecolor, edgecolor=edgecolor)

    # Get grid points within regions
    ilat_in, ilon_in = np.where(mask['mask'] > 1)

    for ilat, ilon in zip(ilat_in, ilon_in):
        place_id = int(mask['mask'][ilat, ilon])
        if len(mask.lat.dims) > 1:
            lat, lon = mask.lat[ilat, ilon], mask.lon[ilat, ilon]
        else:
            lat, lon = mask.lat[ilat], mask.lon[ilon]
        ax.scatter(lon, lat, s=markersize,
                   transform=ccrs.Geodetic(),
                   c=COLORS[place_id % len(COLORS)])
    mask_in = mask.mask[ilat_in, ilon_in]
    ax.set_extent([mask_in.lon.min(), mask_in.lon.max(),
                   mask_in.lat.min(), mask_in.lat.max()])
    ax.set_title('{} {} {}'.format(
        med.cfg['area'], med.geo_src.name, data_src.name))

    fig_filename = 'mask{}.{}'.format(data_src.get_mask_postfix(), fig_format)
    fig_filepath = os.path.join(fig_dir, fig_filename)
    if not cfg_plot.get('no_verbose'):
        log.info('Saving figure for {} mask for {} to {}'.format(
            med.geo_src.name, data_src.name, fig_filepath))
    fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_data_source(data_src, per_region=None, **kwargs):
    """ Plot data from a given source.

    :param data_src: Data source.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
      Default is `False`.
    :type data_src: :py:class:`.data_source.DataSourceBase`
    :type per_region: bool

    .. seealso:: :py:func:`plot_regional_dataset`
    """
    fig_dir = data_src.med.cfg.get_plot_directory(data_src, **kwargs)
    info_msg = ' {}'.format(data_src.name)

    # Get data
    data_src.get_data(**kwargs)

    # Plot dataset
    plot_regional_dataset(
        data_src, fig_dir=fig_dir, info_msg=info_msg,
        per_region=per_region, **kwargs)


def plot_output_variable_result(out_var, result_name='result',
                                stage=None, per_region=None, **kwargs):
    """ Plot features of a given output variable.

    :param out_var: Output variable for which to plot features.
    :param result_name: `'feature'` or `'prediction'`.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
      Should be provided for `'fit'`. Default is `None`.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
      Default is `False`.
    :type out_var: :py:class:`.component.OutputVariable`
    :type result_name: str
    :type stage: str

    .. seealso:: :py:func:`plot_regional_dataset`
    """
    # Get data
    info_msg = ' {}'.format(result_name)
    if result_name == 'feature':
        # Plot feature
        # Make sure that result is loaded and get data
        out_var.extract_feature(stage, **kwargs)
        data_src = out_var.feature[stage]
        if not data_src.data:
            return
        info_msg += ' to {}'.format(stage)
    elif result_name == 'result':
        # Plot prediction or (extracted) output
        # Make sure that result is loaded and get data
        out_var.get_result(**kwargs)
        data_src = out_var.result
    info_msg += ' {}'.format(out_var.comp.name)
    fig_dir = data_src.med.cfg.get_plot_directory(out_var.comp, **kwargs)

    plot_regional_dataset(data_src, fig_dir=fig_dir, info_msg=info_msg,
                          per_region=per_region, **kwargs)


def plot_regional_dataset(data_src, fig_dir='', info_msg='', per_region=None,
                          **kwargs):
    """Plot all variables of a regional dataset.

    :param data_src: Dataset.
    :param fig_dir: Directory in which to save figure.
    :param info_msg: Log and title information message.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
      Default is `False`.
    :type data_src: mapping
    :type fig_dir: str
    :type info_msg: str
    :type per_region: bool
    """
    med = data_src.med
    cfg_plot = load_config(med.cfg, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    per_region = per_region or cfg_plot.get('per_region', False)

    if not cfg_plot.get('no_verbose'):
        log.info('Plotting{} dataset'.format(info_msg))
    for var_name, var in data_src.items():
        if not cfg_plot.get('no_verbose'):
            log.info('Variable: {}'.format(var_name))

        # Define y label with units
        units = var.attrs.get('units')
        sunits = ' ({})'.format(units) if (units and (units != '')) else ''
        ylabel = '{}{}'.format(var_name, sunits)

        # Plot per region
        if not hasattr(var, 'region'):
            # Check if regional data
            var = var.expand_dims(dim='region', axis=-1).assign_coords(
                region=['all'])
        for ir, reg_label in enumerate(var.indexes['region']):
            plot_postfix = '_{}'.format(reg_label) if per_region else ''
            reg_msg = ' - {}'.format(reg_label) if per_region else ''
            if per_region or (ir == 0):
                fig, ax = plt.subplots(1, 1)
                time = var.indexes['time']
                try:
                    for comp_name in var.indexes['component']:
                        label = '{} {}'.format(comp_name, reg_label)
                        ax.plot(time, var.loc[{
                            'region': reg_label, 'component': comp_name}],
                            label=label)
                except KeyError:
                    ax.plot(time, var.loc[:, reg_label], label=reg_label)
            last = (ir == len(var.indexes['region']) - 1)
            if not per_region and last:
                ax.legend(loc='best')
            if per_region or last:
                # Set axes
                ax.set_xlim(time[0], time[-1])
                ax.set_xlabel('time', fontsize=cfg_plot['fs_default'])
                ax.set_ylabel(ylabel, fontsize=cfg_plot['fs_default'])
                ax.set_title('{}{}{}'.format(
                    med.cfg['area'], reg_msg, info_msg))

                # Save figure
                result_postfix = data_src.get_data_postfix(
                    variable=var_name, **kwargs)
                fig_filename = '{}_{}{}{}.{}'.format(
                    var_name, med.cfg['area'], result_postfix, plot_postfix,
                    fig_format)
                fig_filepath = os.path.join(fig_dir, fig_filename)
                if not cfg_plot.get('no_verbose'):
                    log.info('Saving figure to {}'.format(fig_filepath))
                fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_generation_feature(out_var, stage=None, **kwargs):
    """Plot generation features of a given output variable.

    :param out_var: Output variable for which to plot features.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
      Should be provided Default is `None`.
    :type out_var: :py:class:`.component.OutputVariable`
    :type stage: str
    """
    # Plot
    med = out_var.med
    cfg_plot = load_config(med.cfg, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    fig_dir = med.cfg.get_plot_directory(out_var.comp, **kwargs)
    os.makedirs(fig_dir, exist_ok=True)

    if not cfg_plot.get('no_verbose'):
        log.info('Plotting features to {} {}'.format(
            stage, out_var.name))

    # Get data
    out_var.extract_feature(stage)
    data_src = out_var.feature[stage]
    if not data_src.data:
        return
    result_postfix = data_src.get_data_postfix(**kwargs)

    # Configure
    units = {'day': 'Wh/d', 'hour': 'Wh/h'}[med.cfg['frequency']]
    sample_dict = {'hour': 'H', 'day': 'D', 'week': 'W', 'month': 'M',
                   'year': 'Y'}
    sampling = sample_dict[cfg_plot['frequency']]

    # Define groups to plot
    if out_var.comp.name == 'pv':
        groups = {
            # 'irradiance': {
            #     'Irradiance (' + units + '/m2)':
            #     ['global_horizontal_et', 'global_horizontal_surf',
            #      'glob_tilted_surf']},
            'generation': {
                'PV Generation (' + units + ')': ['generation'],
                'Cell Efficiency': ['cell_efficiency']},
            'capacity_factor': {
                'Capacity Factor': ['capacity_factor']}
        }
    elif out_var.comp.name == 'wind':
        groups = {
            'generation': {
                'Wind Generation (' + units + ')': ['generation']},
            'capacity_factor': {
                'Capacity Factor': ['capacity_factor']}
        }

    # Get regions
    ds = data_src[list(list(groups.items())[0][1].items())[0][1][0]]
    regions = ds.indexes['region']

    # Plot for each region
    for reg_label in regions:
        plot_postfix = '_{}_{}'.format(reg_label, cfg_plot['frequency'])

        # Plot per groups
        for group_name, group in groups.items():
            fig = plt.figure()
            ax0 = fig.add_subplot(111)
            for k, (label, var_names) in enumerate(group.items()):
                ax = ax0 if k == 0 else ax0.twinx()
                for iv, var_name in enumerate(var_names):
                    da_reg = data_src[var_name].loc[{'region': reg_label}]
                    da = da_reg.resample(time=sampling).mean(
                        'time', keep_attrs=True)
                    tm = da.indexes['time']
                    ic = (k * len(var_names) + iv) % len(COLORS)
                    ax.plot(tm, da, label=da.attrs.get('long_name'),
                            color=COLORS[ic])
                ax.set_ylabel(label, fontsize=cfg_plot['fs_default'],
                              color=COLORS[k])
                if len(var_names) > 1:
                    ax.legend()
            ax0.set_xticks(ax.get_xticks()[::2])
            ax0.set_xlim(tm[0], tm[-1])
            ax0.set_xlabel('time', fontsize=cfg_plot['fs_default'])
            ax0.set_title('{} - {} {} {} {}'.format(
                med.cfg['area'], reg_label, out_var.comp.name, stage,
                cfg_plot['frequency']))
            fig_filename = '{}_{}{}{}.{}'.format(
                group_name, med.cfg['area'], result_postfix, plot_postfix,
                fig_format)
            fig_filepath = os.path.join(fig_dir, fig_filename)
            if not cfg_plot.get('no_verbose'):
                log.info('Saving figure to {}'.format(fig_filepath))
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_regional_generation_observation(med):
    # Plot
    fig_dir = med.cfg.get_plot_directory(comp, **kwargs)
    os.makedirs(fig_dir, exist_ok=True)

    for var_name in df_cap.columns.levels[0]:
        log.info(var_name)
        df_cap[var_name].plot()
        plt.xlim(years[0], years[-1])
        plt.ylabel('Capacity (MW)', fontsize=cfg['plot']['fs_default'])
        filename = var_name + 'Capacity_GSE_' + cfg['area']
        figpath = os.path.join(fig_dir, filename)
        plt.savefig(figpath, **cfg['plot']['savefigs_kwargs'])

    for var_name in df_gen.columns.levels[0]:
        log.info(var_name)
        df_gen[var_name].plot()
        plt.xlim(years[0], years[-1])
        plt.ylabel('Generation (GWh)', fontsize=cfg['plot']['fs_default'])
        filename = var_name + 'Generation_GSE_' + cfg['area']
        figpath = os.path.join(fig_dir, filename)
        plt.savefig(figpath, **cfg['plot']['savefigs_kwargs'])

    for var_name in df_cf.columns.levels[0]:
        log.info(var_name)
        (df_cf[var_name] * 100).plot()
        plt.xlim(years[0], years[-1])
        plt.ylabel('Capacity Factor (%)',
                   fontsize=cfg['plot']['fs_default'])
        filename = var_name + 'CF_GSE_' + cfg['area']
        figpath = os.path.join(fig_dir, filename)
        plt.savefig(figpath, **cfg['plot']['savefigs_kwargs'])
    if cfg['plot']['show']:
        plt.show(block=False)


def plotRegionalDemandPrediction(cfg):
    al = 0.3
    fig_dir = os.path.join(cfg['plot_dir'], 'demand')
    os.makedirs(fig_dir, exist_ok=True)
    dayType = {'work': 'Working days', 'sat': 'Saturdays',
               'off': 'Sundays and holidays'}
    regions = X[mask_name]

    cal = cfg['calendar'](X.indexes['time'])

    # Get common time slice
    commonIndex = dem.indexes['time']
    commonIndex = commonIndex.intersection(X.indexes['time'])
    time_slice = slice(commonIndex[0], commonIndex[-1])

    # Select
    dem_sel = dem.sel(time=time_slice)
    ds_pred_sel = ds_pred.sel(time=time_slice)
    temp_sel = temp.sel(time=time_slice)
    cal_sel = cfg['calendar'](commonIndex)

    # Get daily averages
    log.info('Computing daily means')
    temp_sel = temp_sel.resample(time='D').mean('time', keep_attrs=True)
    ds_pred_sel = ds_pred_sel.resample(time='D').sum('time', keep_attrs=True)
    dem_sel = dem_sel.resample(time='D').sum('time', keep_attrs=True)
    if cfg['frequency'] == 'hour':
        cal_sel = cal_sel[::24]

    if cfg['fit']['method'] == 'BayesianRidge':
        predName = 'demand_mean'
    else:
        predName = 'demand_prediction'

    for reg_label in regions.values:
        x = temp_sel.loc[{mask_name: reg_label}].values
        y = dem_sel.loc[{mask_name: reg_label}].values
        time_slice = slice(commonIndex[0], commonIndex[-1])
        y_pred = (ds_pred_sel[predName]
                  .loc[{mask_name: reg_label}].values) / 1.e3
        if cfg['fit']['method'] == 'BayesianRidge':
            y_std = (ds_pred_sel['demand_std']
                     .loc[{mask_name: reg_label}].values) / 1.e3

        # Plot model
        log.info('Plotting for region {}'.format(reg_label))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # ect input observations and scale
        for d, (day, dayLabel) in enumerate(dayType.items()):
            # ect variables
            id_day = cal_sel == day

            # Plot prior data
            x_day, y_day = x[id_day], (y[id_day] / 1.e3)
            ax.scatter(x_day, y_day, s=10, label=dayLabel)

            # Plot prediction (with standard deviation if Bayes)
            isort = np.argsort(x_day)
            x_days = x_day[isort]
            y_pred_days = y_pred[id_day][isort]
            if cfg['fit']['method'] == 'BayesianRidge':
                y_std_days = y_std[id_day][isort]
                ax.fill_between(x_days, y_pred_days - y_std_days,
                                y_pred_days + y_std_days,
                                alpha=al, color=COLORS[d])
            ax.plot(x_days, y_pred_days, linewidth=2, linestyle='-')
        ylim = ax.get_ylim()
        # xlim = ax.get_xlim()
        xlim = [-5., 35.]
        # Plot thresholds
        ax.plot([t_heat, t_heat], ylim, '--k', linewidth=2)
        ax.plot([t_cool, t_cool], ylim, '--k', linewidth=2)
        ax.set_xlim(xlim[0], xlim[-1])
        ax.set_ylim(ylim[0], ylim[-1])
        ax.set_xlabel(r'$T\/({}^\circ C)$', fontsize=cfg['plot']['fs_latex'])
        ax.set_ylabel(r'$D\/(GWh/d)$', fontsize=cfg['plot']['fs_latex'])
        # ax.set_title(reg_label)
        # plt.legend()
        prefix = 'demandTemperature_' + cfg['fit']['method']
        source = cfg['data']['source']['climate']
        cfg_src = cfg[source]
        fig_name = 'demand_' + cfg['fit']['method'] + modifier_name + \
            '_' + cfg['climate']['get_climate_path'](cfg_src) + \
            '_' + cfg['area'] + '_' + \
            cfg['frequency'] + '_' + reg_label + '.png'
        figpath = os.path.join(fig_dir, fig_name)
        fig.savefig(figpath, **cfg['plot']['savefigs_kwargs'])
    if cfg['plot']['show']:
        plt.show(block=False)


def plot_roughness(cfg, roughness):
    fig_dir = os.path.join(cfg['plot_dir'], 'climate')
    os.makedirs(fig_dir, exist_ok=True)
    log.info('Plotting')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.pcolormesh(roughness.lon, roughness.lat, roughness.values)
    fig.colorbar(im, ax=ax)
    fig_name = 'roughness_length' + postfix
    figpath = os.path.join(fig_dir, fig_name)
    fig.savefig(figpath, **cfg['plot']['savefigs_kwargs'])


def plot_entsoe(cfg):
    fig_dir = os.path.join(cfg['plot_dir'], 'generation')
    os.makedirs(fig_dir, exist_ok=True)
    log.info('Plotting')
    # Loop over variables
    for da_name, da in col.items():
        log.info(da_name)
        # Loop over sources
        for var_name in da.cooropt.input_data['source'].values:
            log.info(var_name)
            var = da.sel(source=var_name)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            # Loop over regions
            for reg_label in var.cooropt.input_data['region'].values:
                ax.plot(var.time, var.loc[{'region': reg_label}],
                        label=reg_label)
            if len(var.cooropt.input_data['region']) > 1:
                plt.legend(loc='best')
            ylim = ax.get_ylim()
            ax.set_ylim(0., ylim[-1] * 1.1)
            ax.set_xlim(var.indexes['time'][0], var.indexes['time'][-1])
            fig_name = 'entsoe_' + da_name + '_' + var_name + postfix + \
                '.' + cfg['plot']['figFormat']
            figpath = os.path.join(fig_dir, fig_name)
            fig.savefig(figpath, **cfg['plot']['savefigs_kwargs'])

    if cfg['plot']['show']:
        plt.show(block=False)


def plot_opsd(cfg):
    log.info('Plotting')
    for (k, da) in enumerate(data):
        # Resample to monthly
        da_month = da.resample(time='M').sum('time', keep_attrs=True)
        t = da_month.indexes['time']

        fig_dir = os.path.join(cfg['plot_dir'], directories[k])
        os.makedirs(fig_dir, exist_ok=True)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for reg_label in da_month.region.values:
            ax.plot(t, da_month.loc[:, reg_label], label=reg_label)
        ax.legend(loc='best')
        ylabel = '{} ({})'.format(da_month.name, da.units)
        ax.set_ylabel(ylabel, fontsize=cfg['plot']['fs_default'])
        ax.set_xlim(t[0], t[-1])
        ax.set_xticks(ax.get_xticks()[::2])
        fmt = (da.name, 'OPSD', cfg['area'],
               cfg['frequency'], cfg['plot']['figFormat'])
        filename = '{}_{}_{}_{}.{}'.format(*fmt)
        figpath = os.path.join(fig_dir, filename)
        fig.savefig(figpath, **cfg['plot']['savefigs_kwargs'])

    if cfg['plot']['show']:
        plt.show(block=False)


def plot_rte_data(cfg):
    log.info('Plotting')
    plotDir = os.path.join(cfg['plot_dir'], 'generation')
    os.makedirs(plotDir, exist_ok=True)

    # Resample
    gen = da_gen.resample(time='1M').mean('time', keep_attrs=True)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for (iv, v) in enumerate(gen['variable'].values):
        ax.plot(gen.indexes['time'], gen.sel(variable=v),
                color=COLORS[iv], linestyle='-',
                label='generation ' + v)
        ax.plot(da_cap.indexes['time'], da_cap.sel(variable=v),
                color=COLORS[iv], linestyle='--',
                label='capacity ' + v)
    plt.legend()

    if cfg['plot']['show']:
        plt.show(block=False)


def plot_rte_open(cfg):
    log.info('Plotting')
    # Read shapes
    sf = shapefile.Reader(os.path.join(data_dir, ds_name_gen))

    # Loop over the variables
    for field, df_cf in d.items():
        # Get collection
        ptchs, values = [], []
        for sr in sf.iterShapeRecords():
            shape, record = sr.shape, sr.record
            rec_val = df_cf.loc[record[0], record[2]] * 100

            # Add a shape only if the record is valid
            # and corresponds to the selected year
            if (rec_val is None) or (record[0] != cfg_src['plotYear']):
                continue

            # Add all patches of shape
            parts = list(shape.parts) + [len(shape.points)]
            for ip in range(len(shape.parts)):
                ptchs.append(patches.Polygon(
                    shape.points[parts[ip]:parts[ip+1]]))
                values.append(rec_val)
        col = PatchCollection(ptchs, edgecolor='k', linewidths=.1)
        col.set(array=np.array(values), cmap=rcParams['image.cmap'])

        # Plot figure for the record
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.add_collection(col)
        ax.autoscale()
        ax.set_xlim(sf.bbox[0], sf.bbox[2])
        ax.set_ylim(sf.bbox[1], sf.bbox[3])
        ax.axis('off')
        cbar = fig.colorbar(col)
        cbar.ax.set_title('%', fontsize=cfg['plot']['fs_default'])

        # Save figure
        filename = ds_name_cf + '_' + field + '_' + source + '_' + \
            cfg_src['area'] + '_' + cfg_src['plotYear'] + \
            '.' + cfg['plot']['figFormat']
        figpath = os.path.join(fig_dir, filename)
        plt.savefig(figpath, **cfg['plot']['savefigs_kwargs'])

    if cfg['plot']['show']:
        plt.show(block=False)


def plot_geo_dist(
        opt, lat, lon, capa_pv, capa_wind, mean_penetration=None,
        margin=2., alpha=1., n_markers=4, ms_max=1300., capa_max=10000.,
        trans=0.006, crs=None, facecolor=None, edgecolor=None,
        text=False, units='MW', text_format='{:.1f}'):
    """ Plot geographical and technological distribution of RES capacity.

    :param opt: Optimizer.
    :param lat: Mean latitude of the regions.
    :param lon: Mean longitude of the regions.
    :param capa_pv: PV capacities.
    :param capa_wind: Wind capacities.
    :param cfg_plot: Plot configuration.
    :param mean_penetration: Penetration rate to add as annotation.
      Default is `None`, in which case no annotation is added.
    :param margin: Margin at the borders of the plot.
      Default is `2` points.
    :param alpha: Alpha value for the markers colors.
      Default is `1`.
    :param n_markers: Number of markers in legend.
      Default is `4`.
    :param ms_max: Maximum marker size.
      Default is `1300`.
    :param capa_max: Maximum capacity in legend.
      Default is `10000`.
    :param trans: Translation factor to seperate
      markers of the different technologies. Default is `0.006`.
    :param crs: Coordinate Reference System. Default is
      :py:class:`cartopy.crs.LambertAzimuthalEqualArea`.
    :param facecolor: Face color of the regions. Default is `'moccasin'`.
    :param edgecolor: Edge color of the regions. Default is `'dimgrey'`.
    :param text: Whether to add text boxes. Default is False.
    :param units: The units of the given data.
    :param text_format: Format of the text boxes.:type opt: :py:class:`.optimization.OptimizerBase`
    :type lat: sequence
    :type lon: sequence
    :type capa_pv: sequence
    :type capa_wind: sequence
    :type cfg_plot: dict
    :type mean_penetration: float
    :type margin: float
    :type alpha: float
    :type n_markers: int
    :type ms_max: float
    :type capa_max: float
    :type trans: float
    :type crs: :py:class:`cartopy.crs.ABCMeta`
    :type facecolor: str
    :type edgecolor: str
    :type text: bool
    :type units: str
    :type text_format: str
    """
    cfg_plot = load_config(opt.med.cfg, 'plot')
    facecolor = facecolor or cfg_plot.get('region_facecolor') or 'moccasin'
    edgecolor = edgecolor or cfg_plot.get('region_edgecolor') or 'dimgrey'
    crs = crs or ccrs.LambertAzimuthalEqualArea()

    # Convert geometry to CRS
    opt.med.geo_src.get_data()
    gdf_crs = opt.med.geo_src.get(GEO_VARIABLE).to_crs(crs.proj4_init)

    fig = plt.figure(figsize=[12, 9])
    ax = plt.axes(projection=crs)
    ax.set_xlabel('Longitude', fontsize=cfg_plot['fs_default'])
    ax.set_ylabel('Latitude', fontsize=cfg_plot['fs_default'])

    # Plot regions
    gdf_crs.plot(ax=ax, facecolor=facecolor, edgecolor=edgecolor)

    # capa_max = np.max([capa_pv.max(), capa_wind.max()])
    leg_size = (np.round(np.linspace(0., 1., n_markers + 1)[1:], 2)
                * np.round(capa_max, -int(np.log10(capa_max)) + 1))
    exp = 1
    fact = ms_max / leg_size.max()**exp
    trans *= (lon.max() - lon.min()) / 2
    trans_lon = trans * (lon.max() - lon.min()) / 2
    trans_lat = trans * (lat.max() - lat.min()) / 2

    # Draw capacity
    s = capa_pv**exp * fact
    ax.scatter(lon - trans * np.sqrt(s), lat, s=s, c=COLORS[0],
               marker='o', alpha=alpha, transform=ccrs.Geodetic())

    s = capa_wind**exp * fact
    ax.scatter(lon + trans * np.sqrt(s), lat, s=s, c=COLORS[1],
               marker='o', alpha=alpha, transform=ccrs.Geodetic())

    # Add text
    if text:
        for k, (c_pv, c_wind) in enumerate(zip(capa_pv, capa_wind)):
            transform = ccrs.Geodetic()._as_mpl_transform(ax)
            # Annotate PV
            t_lon = lon[k] - 17 * trans_lon
            t_lat = lat[k] - 1.5 * trans_lat
            ax.annotate(text_format.format(c_pv.values), xy=(t_lon, t_lat),
                        xycoords=transform, fontsize='x-large')
            # Annotate wind
            t_lon = lon[k] + 2 * trans_lon
            t_lat = lat[k] - 1.5 * trans_lat
            ax.annotate(text_format.format(c_wind.values), xy=(t_lon, t_lat),
                        xycoords=transform, fontsize='x-large')

    # Draw legend
    h_pv = [plt.plot([-1e9], [-1e9], linestyle='',
                     marker='$\mathrm{PV}$', color='k', markersize=20)[0]]
    h_wind = [plt.plot([-1e9], [-1e9], linestyle='',
                       marker='$\mathrm{Wind}$', color='k', markersize=40)[0]]
    h_pv += [plt.scatter(
        [], [], s=leg_size[s]**exp * fact, c=COLORS[0],
        marker='o', alpha=alpha) for s in np.arange(n_markers)]
    h_wind += [plt.scatter([], [], s=leg_size[s]**exp * fact,
                           c=COLORS[1], marker='o',
                           alpha=alpha) for s in np.arange(n_markers)]
    l_pv, l_wind = [''], ['']
    l_pv += ['' for s in np.arange(n_markers)]
    l_wind += ['{:} MW'.format(int(leg_size[s])) for s in np.arange(n_markers)]
    l_wind += ['{:} {}'.format(int(leg_size[s]), units)
               for s in np.arange(n_markers)]
    ax.legend(h_pv + h_wind, l_pv + l_wind, loc='best', handletextpad=1.,
              labelspacing=2.5, borderpad=1.5, ncol=2, columnspacing=1.5)

    if mean_penetration is not None:
        starget = '$\mu^* = {:.1f}\%$'.format(mean_penetration * 100)
        plt.annotate(starget, xy=(0.7, 0.02), xycoords='axes fraction',
                     fontsize=cfg_plot['fs_latex'])

    # Set extent
    tb = gdf_crs.total_bounds
    extent = tb[0], tb[2], tb[1], tb[3]
    ax.set_extent(extent, crs)

    return fig


def plot_optimization(med, ds, ds_opt):
    """ Plot optimization results.

    :param med: Mediator.
    :type med: :py:class:`.mediator.Mediator`
    """
    cfg = med.cfg
    opt = med.optimizer
    n_reg = int(opt.input_data['n_reg'])
    plot_dir = os.path.join(cfg['plot_dir'], 'optimization')
    os.makedirs(plot_dir, exist_ok=True)
    sratio = ('_ratio{}'.format(int(cfg['constraint']['ratio'] * 100 + 0.1))
              if cfg['constraint']['pv_ratio'] else '')
    mean_pen_rng = np.arange(cfg['penetration']['start'],
                             cfg['penetration']['stop'],
                             cfg['penetration']['step'])

    log.info('Plotting')
    # alpha = 0.2
    # PmismatchStd *= fact
    # PmismatchMean = ds_opt['Pmismatch'].mean('time')

    # # Get the  divers diversification, highest penetration avoiding
    # # critical situations and unconditional penetration scenarios
    # is_val = dscapacity.notnull().all(dim=dim_reg_comp_name)
    # imean_pen_rng = np.nonzero(is_val.values)[0][[0, -1]].tolist()
    # # Get index before shortage or saturation
    # idx_short = np.nonzero((ds_opt['shortage'] > 1.e-2).values)[0].tolist()
    # idx_sat = np.nonzero((ds_opt['saturation'] > 1.e-2).values)[0].tolist()
    # idx_critic = idx_short + idx_sat
    # if len(idx_critic) > 0:
    #     idx = np.min(idx_critic)
    #     imean_pen_rng += [idx - 1]

    # # Plot RES generation per region
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # for r in np.arange(n_reg):
    #     ax.fill_between(mean_pen_rng * 100, PRESMean[:, r] - PRESStd[:, r],
    #                     PRESMean[:, r] + PRESStd[:, r],
    #                     color=COLORS[r], alpha=alpha)
    #     ax.plot(mean_pen_rng * 100, PRESMean[:, r], color=COLORS[r],
    #             linestyle='-', label=str(ds.regionsItaly[r].values))
    # ax.legend(loc='best')
    # ax.set_xlabel('Mean (%)', fontsize=cfg['plot']['fs_default'])
    # ax.set_ylabel('RES Generation (TWh/y)',
    #               fontsize=cfg['plot']['fs_default'])
    # ax.set_xlim(mean_pen_rng[0] * 100, mean_pen_rng[-1] * 100)
    # ax.set_ylim(0., 40.)
    # # ax.set_ylim(-20., 100.)
    # filename = opt_name + postfix + '_RESGen' + '.png'
    # fig_path = os.path.join(plot_dir, filename)
    # fig.savefig(fig_path, dpi=cfg['plot']['dpi'],
    #             bbox_inches=cfg['plot']['bbox_inches'])

    # Plot generation per region and component
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Legend columns titles
    h_pv = [ax.plot([-10.], [-10.], linestyle='',
                    marker='$\mathrm{PV}$', color='k', markersize=40)[0]]
    h_wind = [ax.plot([-10.], [-10.], linestyle='',
                      marker='$\mathrm{Wind}$', color='k', markersize=70)[0]]
    l_pv, l_wind = [''], ['']
    for r in np.arange(n_reg):
        r2 = r + n_reg
        h_pv.append(ax.plot(mean_pen_rng * 100, ds_opt['generation'][:, r],
                            color=COLORS[r], linestyle='-')[0])
        l_pv.append('')
        h_wind.append(ax.plot(mean_pen_rng * 100,
                              ds_opt['generation'][:, r2].values,
                              color=COLORS[r], linestyle='--')[0])
        l_wind.append(str(opt.input_data['region'][r].values))
    ax.legend(h_pv + h_wind, l_pv + l_wind, loc='best', ncol=2,
              columnspacing=.3, handletextpad=0.5, markerscale=0.4)
    ax.set_xlabel('Mean (%)', fontsize=cfg['plot']['fs_default'])
    ax.set_ylabel('Generation (TWh/y)',
                  fontsize=cfg['plot']['fs_default'])
    ax.set_xlim(mean_pen_rng[0] * 100, mean_pen_rng[-1] * 100)
    ax.set_ylim(0., 40.)
    filename = opt_name + postfix + '_generation' + sratio + '.png'
    fig_path = os.path.join(plot_dir, filename)
    fig.savefig(fig_path, dpi=cfg['plot']['dpi'],
                bbox_inches=cfg['plot']['bbox_inches'])

    # Plot PV/Wind ratio
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    h_ratio = ax1.plot(mean_pen_rng * 100, ds_opt['pv_ratio'] * 100,
                       linestyle='-', color=COLORS[0])[0]
    hShort = ax2.plot(mean_pen_rng * 100, ds_opt['shortage'] * 100,
                      linestyle='-', color=COLORS[1])[0]
    hSat = ax2.plot(mean_pen_rng * 100, ds_opt['saturation'] * 100,
                    linestyle='--', color=COLORS[1])[0]
    plt.legend([h_ratio, hShort, hSat],
               ['PV _ratio', 'Shortage', 'Saturation'], loc='best')
    ax1.set_xlabel('Mean (%)', fontsize=cfg['plot']['fs_default'])
    ax1.set_ylabel('PV Ratio (%)', fontsize=cfg['plot']['fs_default'],
                   color=COLORS[0])
    ax2.set_ylabel('Shortage and Saturation (%)',
                   fontsize=cfg['plot']['fs_default'], color=COLORS[1])
    ax1.set_xlim(mean_pen_rng[0] * 100, mean_pen_rng[-1] * 100)
    ax1.set_ylim(0., 100.)
    ax2.set_ylim(0., 12.)
    filename = opt_name + postfix + 'pv_ratio' + sratio + '.png'
    fig_path = os.path.join(plot_dir, filename)
    fig.savefig(fig_path, dpi=cfg['plot']['dpi'],
                bbox_inches=cfg['plot']['bbox_inches'])

    # Mean/Risk plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    # Plot mean/risk
    ax1.plot(ds_opt['risk'] * 100, ds_opt['mean_penetration'] * 100,
             linestyle='-', color=COLORS[0], label='Mean', zorder=1)
    # ax1.scatter((ds_opt['risk'] * 100)[imean_pen_rng],
    # msize = 6
    # (ds_opt['mean_penetration'] * 100)[imean_pen_rng],
    #             s=(msize*1.2)**2, c='k', marker='s', zorder=2)
    # Plot Profit / Risk
    ax2.plot(ds_opt['risk'] * 100, ds_opt['profit'], linestyle='--',
             label='Profit', color=COLORS[1])
    # ds_opt['risk']val = ds_opt['risk'].dropna('target_penetration')
    # ax1.set_xlim(ds_opt['risk']val[0] * 100, ds_opt['risk']val[-1] * 100)
    # ax1.set_xlim(0., 12)
    ax1.set_xlim(0., 29)
    # ax1.set_xlim(9., 15)
    # ax1.set_xlim(12., 20.)
    # Adjust both y-axis limits so that both curves ends match
    ax1.set_ylim(mean_pen_rng[0] * 100, mean_pen_rng[-1] * 100)
    y1min, y1max = ax1.get_ylim()
    y1 = (ds_opt['mean_penetration'] *
          100)[ds_opt['mean_penetration'].notnull()]
    y2 = ds_opt['profit'][ds_opt['profit'].notnull()]
    A = np.array([[y1[-1] - y1min, y1min - y1[0]],
                  [y1[-1] - y1max, y1max - y1[0]]]) / float(y1[-1] - y1[0])
    y2min, y2max = A.dot([y2[0], y2[-1]])
    ax2.set_ylim(y2min, y2max)
    # Mark over transmission
    # idx = np.nonzero((ds_opt['over_transmission'] > 1.e-3).values)[0]
    # if len(idx) > 0:
    #     xlim = ax1.get_xlim()
    #     ax1.fill_between(xlim, y1max,
    # float((ds_opt['mean_penetration'] * 100)[idx[0]]),
    #                      color='0.5', alpha=alpha)
    #     ax1.set_ylim(y1min, y1max)
    # if len(idx_critic) > 0:
    #     xlim = ax1.get_xlim()
    #     ax1.fill_between(xlim, y1max,
    # float((ds_opt['mean_penetration'] * 100)[idx]),
    #                      color='0.5', alpha=alpha)
    #     ax1.set_ylim(y1min, y1max)
    ax1.set_xlabel('Risk (%)', fontsize=cfg['plot']['fs_default'])
    ax1.set_ylabel('Mean (%)', color=COLORS[0],
                   fontsize=cfg['plot']['fs_default'])
    ax2.set_ylabel('Profit (G\u20ac/y)', color=COLORS[1],
                   fontsize=cfg['plot']['fs_default'])
    filename = opt_name + postfix + '_mean_std' + sratio + '.png'
    fig_path = os.path.join(plot_dir, filename)
    fig.savefig(fig_path, dpi=cfg['plot']['dpi'],
                bbox_inches=cfg['plot']['bbox_inches'])

    # # Plot demand response per region
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # for r in np.arange(n_reg):
    #     ax.fill_between(mean_pen_rng * 100,
    #                     PmismatchMean[:, r] - PmismatchStd[:, r],
    #                     PmismatchMean[:, r] + PmismatchStd[:, r],
    #                     color=COLORS[r], alpha=alpha)
    #     ax.plot(mean_pen_rng * 100, PmismatchMean[:, r], linewidth=2,
    #             color=COLORS[r], linestyle='-',
    #             label=str(opt.input_data['region'][r].values))
    # ax.legend(loc='best')
    # ax.set_xlabel('Mean (%)', fontsize=cfg['plot']['fs_default'])
    # ax.set_ylabel('Load - RES (TWh/y)', fontsize=cfg['plot']['fs_default'])
    # ax.set_xlim(mean_pen_rng[0] * 100, mean_pen_rng[-1] * 100)
    # ax.set_ylim(0., 150.)
    # filename = opt_name + postfix + '_Pmismatch' + sratio + '.png'
    # fig_path = os.path.join(plot_dir, filename)
    # fig.savefig(fig_path, dpi=cfg['plot']['dpi'],
    #             bbox_inches=cfg['plot']['bbox_inches'])

    if cfg['plot']['show']:
        plt.show(block=False)


def plot_cf_from_generation_mean_cf(med):
    cfg_plot = load_config(med.cfg, 'plot')

    # Loop over sources
    for varName in daCF.coords['source'].values:
        if cfg['verbose']:
            print(varName)
        var = daCF.sel(source=varName)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # Loop over regions
        for regLabel in var.coords[maskName].values:
            ax.plot(var.time, var.loc[{maskName: regLabel}],
                    label=regLabel)
        ax.set_ylim(0., 1.)
        ax.set_xlim(var.indexes['time'][0], var.indexes['time'][-1])
        figName = 'ENTSOE_GSE_capacity_factor_' + varName + postfix + \
            '.' + cfg['plot']['figFormat']
        figPath = os.path.join(plotDir, figName)
        fig.savefig(figPath, dpi=cfg['plot']['dpi'],
                    bbox_inches=cfg['plot']['bbox_inches'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_band_spectrum(med, ds, filt, time_slice=None,
                       plot_freq=['Y', 'D', 'H'], var_ylims={},
                       add_legend=False, **kwargs):
    """Plot band spectrum, i.e. the integration of power spectrum over
    frequency bands.

    :param med: Mediator.
    :param ds: Dataset of output variables of components.
    :param filt: Filtered data.
    :param time_slice: Period to select.
    :param plot_freq: Frequencies for which to plot.
      Default is `['Y', 'D', 'H']`.
    :param var_ylims: Mapping of y-axis limits to output-variable names.
    :param add_legend: Whether to add the legend. Default is `False`.
    :type med: :py:class:`.mediator.Mediator`
    :type ds: mapping
    :type filt: mapping
    :type time_slice: slice
    :type plot_freq: sequence
    :type var_ylims: mapping
    :type add_legend: bool
    """
    cfg_plot = load_config(med.cfg, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    lw = {'Y': 3, 'D': 2, 'H': 1}
    zo = {'Y': 3, 'D': 2, 'H': 1}
    labels = {'Y': 'Yearly-mean', 'D': 'Daily-mean', 'H': 'Hourly'}
    var_labels = {'demand': '', 'capacity_factor': 'Capacity Factor'}
    comp_labels = {'demand': 'Demand', 'pv': 'PV', 'wind': 'Wind'}
    figsize = kwargs.get('figsize') or rcParams['figure.figsize']
    for comp_name, ds_comp in ds.items():
        comp = med[comp_name]
        fig_dir = med.cfg.get_plot_directory(comp, **kwargs)
        for out_var_name, da in ds_comp.items():
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            filt_var = filt[comp_name][out_var_name]
            for ifr, freq in enumerate(filt_var):
                dum = filt_var[freq]
                if time_slice is not None:
                    dum = dum.sel(time=time_slice)
                if ifr == 0:
                    ts = dum
                else:
                    ts += dum
                if freq in plot_freq:
                    ax.plot(ts.time, ts, linewidth=lw[freq], zorder=zo[freq],
                            label=labels[freq])

            ylabel = '{} {}'.format(
                comp_labels[comp_name], var_labels[out_var_name])
            units = da.attrs.get('units')
            if units:
                ylabel += ' ({})'.format(units)
            elif out_var_name == 'capacity_factor':
                ylabel += ' (%)'
            ax.set_ylabel(ylabel, fontsize=cfg_plot['fs_default'])
            # Add limits
            ylim = var_ylims.get(out_var_name)
            if ylim is not None:
                ax.set_ylim(ylim)

            # Add legend only if regions not present
            if add_legend:
                ax.legend(loc='upper right')

            # Save figure
            res = comp[out_var_name].result
            result_postfix = res.get_data_postfix(**kwargs)
            if time_slice is not None:
                result_postfix += '_{}_{}'.format(
                    time_slice.start, time_slice.stop)
            fig_filename = 'filtered_{}_{}{}.{}'.format(
                res.name, med.cfg['area'], result_postfix, fig_format)
            fig_filepath = os.path.join(fig_dir, fig_filename)
            if not cfg_plot.get('no_verbose'):
                log.info('Saving figure to {}'.format(fig_filepath))
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)

