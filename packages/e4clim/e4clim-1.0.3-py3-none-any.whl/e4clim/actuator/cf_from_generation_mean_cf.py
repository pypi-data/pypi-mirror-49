"""Estimator of capacity factor time series from generation time series
and capacity factor averages."""
import logging
import pandas as pd
import xarray as xr
from ..actuator_base import OutputExtractorBase

#: Logger.
log = logging.getLogger(__name__)


class Actuator(OutputExtractorBase):
    """Estimator of capacity factor time series from generation time series
    and capacity factor averages."""

    def __init__(self, output_variable, cfg=None, **kwargs):
        """Naming constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param cfg: Actuator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type cfg: dict
        """
        name = 'cf_from_generation_mean_cf'
        default_output_variable = 'capacity_factor'
        if output_variable.name != default_output_variable:
            log.warning(
                'Output variable {} given to constructor does not correspond '
                'to {} output variable to be estimated by {}'.format(
                    output_variable.name, default_output_variable,
                    self.name))

        super(Actuator, self).__init__(
            output_variable=output_variable, name=name, cfg=cfg,
            **kwargs)

    def transform(self, data_src, **kwargs):
        """Extract capacity factor time series from generation time series
        and capacity factor averages for component.

        :param data_src: Input data source containing generation
          time series and capacity factor averages.
        :type data_src: :py:class:`.data_source.DataSourceBase`

        :returns: Capacity factor time series.
        :rtype: dict

        .. warning:: Data source should be loaded, e.g. with
          :py:meth:`data_src.get_data`.
        """
        if not self.cfg.get('no_verbose'):
            log.info('Computing {} {} time series from {} gener'
                     'ation time series and {} capacity factor means'.format(
                         self.comp.name, self.output_variable.name,
                         data_src['generation'].name,
                         data_src['capacity_factor'].name))

        # Get generation and capacity factors
        da_gen = data_src['generation'].sel(component=self.comp.name)
        da_cf_mean = data_src['capacity_factor'].sel(component=self.comp.name)

        # Get mean generation
        da_gen_mean = da_gen.resample(
            time=self.cfg['mean_frequency']).mean('time')

        # Get mean capacity
        da_cap_mean = da_gen_mean / da_cf_mean

        # # Get capacity time series by linearly interpolating
        # da_cap = da_cap_mean.resample(time='H').interpolate('linear')

        # Get capacity time series from last year to avoid 2015
        # high generation
        t_cap_mean = da_cap_mean.indexes['time']
        delta_day = pd.Timedelta(23, unit='H')
        start = '{}-01-01'.format(t_cap_mean[0].year + 1)
        end = t_cap_mean[-1] + delta_day
        t_sub = pd.date_range(start=start, end=end, freq='H')
        da_cap = da_cap_mean.reindex(time=t_sub).bfill('time').ffill('time')

        # Get capacity factors time series on intersection
        da_cf_sub = da_gen / da_cap

        if self.cfg.get('extrapolate'):
            t_cf_mean = da_cf_mean.indexes['time']
            start = '{}-01-01'.format(t_cf_mean[0].year)
            end = t_cf_mean[-1] + delta_day
            t_ext = pd.date_range(start=start, end=end, freq='H')
            da_cf = da_cf_sub.reindex(time=t_ext)

            # Compute yearly correctors and apply to missing years
            corrector = da_cf_mean / da_cf_sub.mean('time')
            gp = da_cf.resample(time=self.cfg['mean_frequency'])
            for date, da_date in gp:
                date = pd.Timestamp(date)

                # Correct year
                da_corr = da_cf_sub * corrector.sel(time=date)

                # Remove leap if needed (nan's will be assumed if leap)
                da_corr = da_corr[(da_corr.indexes['time'].date !=
                                   pd.Timestamp('2016-02-29').date())]

                # Index for year
                t_cf_sub = da_corr.indexes['time']
                da_corr['time'] = pd.DatetimeIndex([str(date.year) + str(d)[4:]
                                                    for d in t_cf_sub])

                da_cf.loc[{'time': da_corr.time}] = da_corr
        else:
            da_cf = da_cf_sub

        # Sub-sample, if needed
        if self.med.cfg['frequency'] == 'day':
            da_cf = da_cf.resample(time='D').mean('time')
        else:
            # Compare the variance from the hourly data
            # with that of the daily data
            da_cf_day = da_cf.resample(time='D').mean('time')
            cf_var = da_cf.var('time')
            cf_day_var = da_cf_day.var('time')
            var_ratio = 1. - cf_day_var / cf_var
            if not self.cfg.get('no_verbose'):
                log.info('Extracted {} {} intra-day variance: '.format(
                    self.comp.name, self.output_variable.name))
                log.info(var_ratio.values)

        return xr.Dataset({self.output_variable.name: da_cf})

    def get_output_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_{}'.format(
            super(Actuator, self).get_output_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        if self.cfg.get('extrapolate'):
            postfix += '_extrapolate'

        return postfix
