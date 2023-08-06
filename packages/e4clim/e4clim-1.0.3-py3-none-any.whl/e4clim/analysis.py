"""Various analysis functions."""
import os
import logging
import numpy as np
import pandas as pd
import xarray as xr
from scipy.stats import t
from uncertainties.unumpy import uarray


#: Logger.
log = logging.getLogger(__name__)


def get_band_spectrum(med, region=None, comp_names=None, comp_time_slices={},
                      **kwargs):
    """Get band spectrum, i.e. the integration of power spectrum over
    frequency bands.

    :param med: Mediator.
    :param region: Region to select, `global` or `None`.
      Default is `None`, in which case all regions are kept.
      If `'global'`, data is aggregated over regions.
    :param comp_names: Names of components to select. Default is `None`,
      in which case all components in mediator are selected.
    :param comp_time_slices: Time slice per component.
    :type med: :py:class:`.mediator.Mediator`
    :type region: str
    :type comp_names: collection
    :type comp_time_slices: :py:class:`slice`-valued mutable

    :returns: Original and filtered datasets per component and output variable.
    :rtype: :py:class:`tuple` of mappings
    """
    freqs = ['Y', 'D', 'H']
    ds = {}
    var_tot = {}
    filt = {}
    var_filt = {}

    # Read hourly capacity factors from ENTSO-E and GSE
    comp_names = comp_names or med.components.keys()
    for comp_name in comp_names:
        # Get result
        comp = med.components[comp_name]
        comp.get_result(**kwargs)
        file_dir = med.cfg.get_project_data_directory(comp, **kwargs)
        time_slice = comp_time_slices.get(comp_name)

        ds[comp_name] = {}
        var_tot[comp_name] = {}
        filt[comp_name] = {}
        var_filt[comp_name] = {}
        for out_var_name in comp.output_variables.keys():
            # Get array for variable
            da = comp.result[out_var_name]

            # Select time slice if needed
            if time_slice is not None:
                da = da.sel(time=time_slice)

            coords = [('frequency', freqs)]
            coords_shape = (len(freqs),)
            if region is not None:
                # Select region
                da = (da.sum('region') if region == 'global' else
                      da.loc[{'region': region}])
            else:
                coords.append(da.coords['region'])
                coords_shape += (len(da.coords['region']),)
            ds[comp_name][out_var_name] = da

            # Get the total variance of each variable
            var_tot[comp_name][out_var_name] = da.var('time')

            # Loop over the sampling frequencies
            high_pass = da.copy(deep=True)
            log.info('Filtering {}'.format(comp_name))
            filt[comp_name][out_var_name] = {}
            var_filt[comp_name][out_var_name] = xr.DataArray(
                np.zeros(coords_shape), coords=coords)
            for freq in freqs:
                log.info('- Frequency: {}'.format(freq))
                if freq != 'H':
                    # Low-pass filter
                    low_pass = high_pass.resample(time=freq).mean('time')
                    # Up-sample
                    t = low_pass.indexes['time']
                    if freq == 'Y':
                        low_pass = low_pass.reindex(
                            time=high_pass.indexes['time'],
                            method='bfill').ffill('time')
                    else:
                        new_index = pd.to_datetime({
                            'year': t.year, 'month': t.month, 'day': t.day,
                            'hour': 0.})
                        low_pass = low_pass.reindex(time=new_index)
                        low_pass = low_pass.reindex(
                            time=high_pass.indexes['time'], method='ffill')
                    # High-pass filter
                    high_pass -= low_pass
                else:
                    low_pass = high_pass

                # Store filtered data
                filt[comp_name][out_var_name][freq] = low_pass

                # Get the variance
                var_filt[comp_name][out_var_name].loc[freq] = low_pass.var(
                    'time') / var_tot[comp_name][out_var_name]
                var_filt[comp_name][out_var_name].attrs['units'] = ''
                var_filt[comp_name][out_var_name].name = 'band_spectrum'

                # Write result
                res = comp[out_var_name].result
                result_postfix = res.get_data_postfix(**kwargs)
                filename = 'band_spectrum_{}_{}{}.nc'.format(
                    res.name, med.cfg['area'], result_postfix)
                filepath = os.path.join(file_dir, filename)
                log.info('Writing {} {} band spectrum to {}'.format(
                    comp_name, out_var_name, filepath))
                var_filt[comp_name][out_var_name].to_netcdf(filepath)

    # Print results
    prec = 1
    np.set_printoptions(precision=prec)
    log.info('Component\tVariable\tFrequency Range\tVariance (%)')
    for comp_name in comp_names:
        comp = med.components[comp_name]
        for out_var_name in comp.output_variables.keys():
            for freq in freqs:
                val = var_filt[comp_name][out_var_name].loc[freq].values * 100
                log.info('{}\t{}:'.format(comp_name, freq))
                log.info(val)

    log.info('Component\tVariable\tFrequency Range\tStandard Deviation (%)')
    for comp_name in comp_names:
        comp = med.components[comp_name]
        for out_var_name in comp.output_variables.keys():
            for freq in freqs:
                val = xr.ufuncs.sqrt(
                    var_filt[comp_name][out_var_name].loc[freq].values) * 100
                log.info('{}\t{}:'.format(comp_name, freq))
                log.info(val)

    return (ds, filt)


def compare_yearly_covariance(med_ref, med_new, comp_names=None, **kwargs):
    dim_comp_reg_name = 'component_region'

    # Read hourly capacity factors from ENTSO-E and GSE
    comp_names = comp_names or set(med_ref.components.keys()).intersection(
        med_ref.components.keys())
    for comp_name in comp_names:
        ref_mean, ref_risk = get_mean_risk(med_ref, comp_name)
        new_mean, new_risk = get_mean_risk(med_new, comp_name)

        # Compute the probability to find the observed moment
        # in the Gaussian distribution fitted to the moments
        # computed from the climate data
        q = 0.05
        # For the mean
        ref_mean_like = xr.zeros_like(ref_mean)

        n = new_mean.shape[0]

        # Loop over all dimensions
        for it in ref_mean_like.coords['time']:
            for k in ref_mean_like.coords[dim_comp_reg_name]:
                loc = {'time': it, dim_comp_reg_name: k}
                # Fit a normal distribution to the climate moments
                x = new_mean.loc[{dim_comp_reg_name: k}]
                s = x.std(ddof=1)
                ref_mean_like.loc[loc] = - t.ppf(
                    q/2, df=n - 1, scale=s * np.sqrt(1+1/n))

        # For the covariance
        ref_risk_like = xr.zeros_like(ref_risk)
        # Loop over all dimensions
        for it in ref_risk_like.coords['time']:
            for k in ref_risk_like.coords[dim_comp_reg_name]:
                loc = {'time': it, dim_comp_reg_name: k}
                # Fit a normal distribution to the climate moments
                x = new_risk.loc[{dim_comp_reg_name: k}]
                s = x.std(ddof=1)
                ref_risk_like.loc[loc] = -t.ppf(
                    q/2, df=n - 1, scale=s * np.sqrt(1+1/n))

        # Check which risk observations fall inside the confidence interval
        inside = ((ref_risk.mean('time') > (
            new_risk.mean('time') - ref_risk_like.mean('time'))) &
            (ref_risk.mean('time') < (
                new_risk.mean('time') + ref_risk_like.mean('time'))))

        prec = 1
        np.set_printoptions(precision=prec)
        log.info('risk for {}'.format(comp_name))
        log.info('Observed:')
        log.info(ref_risk.mean('time').sel(comp_name=comp_name).values * 100)
        log.info('Computed:')
        ua = uarray((new_risk.mean('time').sel(comp_name=comp_name)
                     .values * 100).round(prec),
                    (ref_risk_like.mean('time').sel(comp_name=comp_name)
                     .values * 100).round(prec))
        s = '['
        for (k, (u, ins)) in enumerate(
                zip(ua, inside.sel(comp_name=comp_name).values)):
            s += repr(u)
            s += ', ' if k < (len(ua) - 1) else ''
        s += ']'
        log.info(s)


def get_mean_risk(med, comp_name, **kwargs):
    dim_comp_reg_name = 'component_region'
    dim_comp_reg = {dim_comp_reg_name: (
        'component', 'region_multi')}

    # Get result
    comp_ref = med.components[comp_name]
    comp_ref.get_result(**kwargs)
    da = comp_ref.result[med.cfg['components'][comp_name]]

    # Expand component dimension
    da = da.expand_dims('component').assign_coords(
        component=[comp_name])

    # Remove NaNs
    da = da[~da.isnull().any(['region'])]

    # Stack
    da = da.stack(**dim_comp_reg)
    coord_comp_reg = da.coords[dim_comp_reg_name]
    n_comp_reg = len(coord_comp_reg)

    # Sub-sample, if needed
    if med.cfg['frequency'] == 'day':
        da = da.resample(time='D').mean('time')

    # Get mean capacity factors for each year
    gp = da.resample(time='Y')
    da_mean = gp.mean('time')

    # Get the capacity factor covariances for each year
    time = pd.to_datetime(list(gp.groups))
    coords = [('time', time), coord_comp_reg]
    da_risk = xr.DataArray(np.empty((time.shape[0], n_comp_reg)),
                           coords=coords)
    for year, group in gp:
        da_risk.loc[{'time': year}] = group.std('time')

    return da_mean, da_risk
