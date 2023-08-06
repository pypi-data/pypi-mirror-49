"""Bias corrector and predictor."""
import logging
from numpy import set_printoptions
import pandas as pd
from sklearn.exceptions import NotFittedError
from ..actuator_base import EstimatorBase

#: Logger.
log = logging.getLogger(__name__)


class Actuator(EstimatorBase):
    """Bias corrector and predictor."""

    def __init__(self, output_variable, cfg=None, **kwargs):
        """Naming constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param cfg: Actuator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type cfg: dict
        """
        name = 'bias_corrector'
        super(Actuator, self).__init__(
            output_variable=output_variable, name=name, cfg=cfg,
            **kwargs)

    def fit(self, data_src_in, data_src_out, **kwargs):
        """Get bias corrector for component as a factor to multiply the
        input data with and such that the training input data
        multiplied by the bias corrector has the same mean
        as the training output data over the same period.

        :param data_src_in: Training set input data source.
        :param data_src_out: Training set output data source.
        :type data_src_in: :py:class:`.data_source.DataSourceBase`
        :type data_src_out: :py:class:`.data_source.DataSourceBase`
        """
        da_in = data_src_in[self.output_variable.name]
        da_out = data_src_out[self.output_variable.name]
        # Try to select component in case needed
        try:
            da_in = da_in.sel(component=self.comp.name)
        except ValueError:
            pass
        try:
            da_out = da_out.sel(component=self.comp.name)
        except ValueError:
            pass

        # Select input period as given by configuration or first full years
        da_in, time_slice_in = self.select_period_from_array(da_in, 'in')

        # Select output period as given by configuration or first full years
        da_out, time_slice_out = self.select_period_from_array(da_out, 'out')

        # Check if selected period intersects that of input period
        if self.cfg.get('intersection_only_if_possible'):
            inter_slice = intersection_time_slice(da_in, da_out)
            if inter_slice is not None:
                time_slice_in = time_slice_out = inter_slice

        # Get bias corrector
        if not self.cfg.get('no_verbose'):
            log.info('Computing {} {} bias corrector'.format(
                self.output_variable.name, self.comp.name))
        mean_in = da_in.sel(time=time_slice_in).mean('time')
        mean_out = da_out.sel(time=time_slice_out).mean('time')
        bc = mean_out / mean_in

        # Convert coordinates datatypes from object to str if needed
        for dim in bc.dims:
            if bc[dim].dtype == object:
                bc[dim] = bc[dim].astype(str)
        self.coef = bc

        set_printoptions(precision=3)
        if not self.cfg.get('no_verbose'):
            log.info('Computed average ({} / {}):'.format(
                time_slice_in.start, time_slice_in.stop))
            log.info(mean_in.values)
            log.info('Observed average ({} / {}):'.format(
                time_slice_out.start, time_slice_out.stop))
            log.info(mean_out.values)

    def predict(self, data_src_in, **kwargs):
        """Apply bias corrector for component by multipling input data.

        :param data_src_in: Input data source.
        :type data_src_in: :py:class:`..data_source.DataSourceBase`

        :returns: Bias corrected dataset.
        :rtype: dict
        """
        ds = {}
        # Verify that bias corrector has been fitted
        if self.coef is None:
            raise NotFittedError('This bias corrector instance '
                                 'must be fitted before prediction.')

        # Select output variable
        da_in = data_src_in[self.output_variable.name]
        try:
            # Try to select component if needed in both data sources
            da_in = da_in.sel(component=self.comp.name)
        except ValueError:
            pass

        # Copy input dataset
        da_pred = da_in.copy(deep=True)

        # Reorder regions to comply and try to select component
        # in case needed
        coef_comp = self.coef.loc[{'region': da_in.indexes['region']}]
        try:
            coef_comp = coef_comp.sel(component=self.comp.name)
        except ValueError:
            pass

        # Apply bias corrector,
        # with input data
        da_pred *= coef_comp

        # Add bias-corrected output variable to dataset
        ds[self.output_variable.name] = da_pred

        return ds

    def select_period_from_array(self, da, data_type):
        """Select full years period from an array.
        Try to get first and last dates from configuration.
        Otherwise, select the first full years.

        :param da: Array.
        :param data_type: `'in'` or '`out`' data type for which
          to get dates in configuration.
        :type da: :py:class:`xarray.DataArray`
        :type data_type: str

        :returns: Tuple containing the selected array and time slice.
        :rtype: :py:class:`tuple` of :py:class:`xarray.DataArray`
          and :py:class:`slice`
        """
        # Get time index
        time = da.indexes['time']

        # First date is given or first available date
        first_date = pd.Timestamp(
            self.cfg.get('first_date_{}'.format(data_type)) or
            time[0])

        # Last date is given or last date which is a multiple of one
        # year past first date
        last_date = pd.Timestamp(
            self.cfg.get('last_date_{}'.format(data_type)) or
            last_full_years_date(time, first_date))

        # Slice
        time_slice = slice(first_date, last_date)
        da = da.sel(time=time_slice)

        return da, time_slice

    def get_estimator_postfix(self, **kwargs):
        """Get bias-corrector postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_nobias'.format(
            super(Actuator, self).get_estimator_postfix(**kwargs))


def last_full_years_date(time, first_date):
    """Get last date in date-time index which is a multiple of a year
    away from start date.

    :param time: Date-time index.
    :param first_date: First date.
    :type time: :py:class:`pandas.DatetimeIndex`
    :type first_date: :py:class:`datetime.date`

    :returns: Last date.
    :rtype: :py:class:`datetime.date`
    """
    last_date = pd.Timestamp(time[-1].year, first_date.month,
                             first_date.day, first_date.hour)
    if last_date not in time:
        last_date = pd.Timestamp(time[-1].year - 1, first_date.month,
                                 first_date.day, first_date.hour)

    return last_date


def intersection_time_slice(da_in, da_out):
    """Get full years intersection between two arrays, if possible.

    :param da_in: First array.
    :param da_out: Second array.
    :type da_in: :py:class:`xarray.DataArray`
    :type da_out: :py:class:`xarray.DataArray`

    :returns: Intersection time slice.
    :rtype: slice
    """
    t_inter = da_out.indexes['time'].intersection(
        da_in.indexes['time'])
    if len(t_inter) > 0:
        first_date_inter = t_inter[0]
        last_date_inter = last_full_years_date(
            t_inter, first_date_inter)
        if ((last_date_inter - first_date_inter)
                >= pd.Timedelta(1, unit='Y')):
            # If there are at least a year of common data,
            # use common data only
            time_slice = slice(first_date_inter, last_date_inter)

            return time_slice
