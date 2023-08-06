"""CORDEX API."""
import os
import logging
from collections import OrderedDict
import ftplib
import numpy as np
import pandas as pd
import xarray as xr
from ..container import ensure_collection
from ..grid import GriddedDataSourceBase

#: Logger.
log = logging.getLogger(__name__)


class DataSource(GriddedDataSourceBase):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        name = name or 'cordex'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, variables=None, **kwargs):
        """Download cordex data and save it locally.

        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :type variables: (collection of) :py:class:`str`
        """
        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        # Define data directories
        sim_dir = self._get_sim_dir()

        # Get credentials
        cred = self.med.cfg.get_credentials(self.name, keys=['user', 'passwd'])

        # Login to the FTP server
        ftp = ftplib.FTP(self.cfg['server'])
        ftp.login(**cred)
        ftp.cwd(sim_dir)

        svar = ', '.join(str(var_name) for var_name in variables)
        if not self.cfg.get('no_verbose'):
            log.info('{} variables for {} simulation'.format(
                svar, sim_dir))
        # Loop over all data-source variables
        for var_name in self.variables:
            # Try to get variable name
            src_var_name = self.cfg['variable_names'].get(var_name)
            if src_var_name is None:
                log.warning("{} variable not in 'variable_names' of {} "
                            "configuration-file: skipping".format(
                                var_name, self.name))
                continue

            # # Download all files for this variable
            # filenames = ftp.nlst(src_var_name)
            # if src_var_name == 'ps':
            #     # Try sea-level pressure instead of surface pressure
            #     src_var_name = 'psl'
            #     filenames = ftp.nlst(src_var_name)
            #     if len(filenames) == 0:
            #       if not self.cfg.get('no_verbose'):
            #           log.info(('\n  No file for variable {}'
            #                  'on server'.format(src_var_name)))
            #         continue
            # else:
            #     continue

            # Loop over periods
            for start_date, end_date in zip(
                    self.cfg['streams']['start_dates'],
                    self.cfg['streams']['end_dates']):
                # Get paths
                var_dir, var_file = self._get_var_dir_file(
                    variable=var_name, start_date=start_date,
                    end_date=end_date)

                # Make local directories
                os.makedirs(var_dir, exist_ok=True)

                filepath = os.path.join(var_dir, var_file)
                ftp.retrbinary('RETR ' + src_var_name + '/' + var_file,
                               open(filepath, 'wb').write)

        # Close
        ftp.close()

    def load(self, transform=None, variables=None, **kwargs):
        """Collect all required variables from cordex simulations.

        :param transform: A function or a composee of functions
          to apply to the datasets.
          These functions should take as arguments a dataset
          and a :py:class:`.data_source.DataSourceBase` data source.
        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :type transform: :py:class:`func` or
          :py:class:`.data_source.Composer`
        :type variables: (collection of) :py:class:`str`

        :returns: A dataset collecting all the variables and periods.
        :rtype: :py:class:`xarray.Dataset`

        .. note::
            * All the variables are first read, then the functions are applied
                and the different periods are finally concatenated.
            * The Med-cordex data is available on the
              `Med-cordex website <https://www.medcordex.eu/>` .

        .. seealso::
            * `cordex variables requirements table <https://www.medcordex.eu/cordex_variables_requirement_table_110628.pdf>`
            * `cordex archive specifications <http://cordex.dmi.dk/joomla/images/cordex/cordex_archive_specifications.pdf>`

        """
        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        # Collect all periods
        ds = xr.Dataset()
        for start_date, end_date in zip(
                self.cfg['streams']['start_dates'],
                self.cfg['streams']['end_dates']):
            # Collect all variables
            ds_per = xr.Dataset()
            for var_name in variables:
                # Get paths
                src_var_name = self.cfg['variable_names'].get(var_name)
                if src_var_name is None:
                    log.warning("{} variable not in 'variable_names' of "
                                "{} configuration-file: skipping".format(
                                    var_name, self.name))
                    continue
                var_dir, var_file = self._get_var_dir_file(
                    variable=var_name, start_date=start_date,
                    end_date=end_date)
                filepath = os.path.join(var_dir, var_file)
                if not self.cfg.get('no_verbose'):
                    log.info('Reading {} from {}'.format(
                        var_name, filepath))

                # Read data
                with xr.open_dataset(filepath) as ds_var:
                    # Select variable of interest to get rid of other variables
                    da = ds_var[src_var_name].squeeze(drop=True)

                    # Ensure that the temperature is in Kelvin
                    if 'temperature' in var_name:
                        if da.mean() < 150.:
                            da += 273.15

                    # Ensure that the pressure is in Pa
                    if 'pressure' in var_name:
                        da *= 10**(5 - np.round(np.log10(da.mean())))

                    # Indexes x and y may change in some data set resulting
                    # in erros when aligning. Just set with integers.
                    if 'y' in da.coords:
                        da['y'] = np.arange(da['y'].shape[0])
                    if 'x' in da.coords:
                        da['x'] = np.arange(da['x'].shape[0])
                    var = da.to_dataset(name=var_name)

                    if self.cfg['height'] not in var[var_name].attrs:
                        # Add height as attribute
                        if self.cfg['height'] in ds_var:
                            var[var_name].attrs['height'] = float(
                                ds_var[self.cfg['height']])
                        elif self.cfg['height'] in ds_var.coords:
                            var[var_name].attrs['height'] = float(
                                ds_var.coords[self.cfg['height']])
                        else:
                            # Assume 2m height
                            var[var_name].attrs['height'] = 2.
                    else:
                        # Rename
                        var[var_name].attrs['height'] = var[
                            var_name].attrs[self.cfg['height']]

                    # Make sure the time indexes are exactly the same
                    # (some variables use 'days since', others
                    # 'hours from',
                    # which is not processed by python netcdf)
                    if 'time' in ds_per:
                        var['time'] = ds_per['time']

                    # Create or add variable
                    ds_per = ds_per.merge(var)

            # Convert time at 12:00:00 to dates
            if self.cfg['frequency'] == 'day':
                td = pd.DatetimeIndex(ds_per.indexes['time'].date)
                ds_per.coords['time'] = td

            # Squeeze in case a one-dimensional level coordinate exists
            ds_per = ds_per.squeeze()

            # Apply functions to the dataset if given
            if transform:
                kwargs.update({'ds': ds_per, 'data_src': self})
                ds_per = transform(**kwargs)

            # Create or add period
            ds = ds.merge(ds_per)

        return ds

    def get_postfix(self, start_date=None, end_date=None, **kwargs):
        """Get standard postfix for cordex data.

        :param start_date: Simulation start-date. Default is `None`, in which
          case the first date of `self.cfg['streams']['start_dates']` is used.
        :param end_date: Simulation end-date. Default is `None`, in which case
          the first date of `self.cfg['streams']['end_dates']` is used.
        :type start_date: str
        :type end_date: str

        :returns: Postfix.
        :rtype: str
        """
        start_date = start_date or self.cfg['streams']['start_dates'][0]
        end_date = end_date or self.cfg['streams']['end_dates'][-1]

        # Get paths
        fmt = (self.cfg['domain'], self.cfg['gcm_model_name'],
               self.cfg['cmip5_experiment_name'],
               self.cfg['cmip5_ensemble_member'],
               self.cfg['rcm_model_name'], self.cfg['rcm_version_id'],
               self.cfg['frequency'], start_date, end_date)
        postfix = '_{}_{}_{}_{}_{}_{}_{}_{}-{}'.format(*fmt)

        return postfix

    def _get_sim_dir(self, **kwargs):
        """Get simulation directory of cordex data.

        returns: Source directory and filename.
        :rtype: tuple of str
        """
        sim_dir = os.path.join(
            self.cfg['domain'], self.cfg['institution'],
            self.cfg['gcm_model_name'],
            self.cfg['cmip5_experiment_name'],
            self.cfg['cmip5_ensemble_member'],
            self.cfg['rcm_model_name'],
            self.cfg['rcm_version_id'], self.cfg['frequency'])

        return sim_dir

    def get_grid(self, *args, **kwargs):
        """Get grid used to make masks.

        :returns: Dataset coordinates.
        :rtype: :py:class:`tuple` of pairs of :py:class:`str`
          and :py:class:`numpy.array`
        """
        var_dir, var_file = self._get_var_dir_file()
        filepath = os.path.join(var_dir, var_file)
        if not self.cfg.get('no_verbose'):
            log.info('Reading sample {} data from {}'.format(
                self.name, filepath))
        with xr.open_dataset(filepath) as ds:
            # Get grid coordinates
            coords = (ds.lat.copy(deep=True).coords
                      if len(ds.lat.shape) > 1 else
                      OrderedDict({
                          'lat': ds.lat.copy(deep=True).values,
                          'lon': ds.lon.copy(deep=True).values}))
        return coords
    
    def get_grid_postfix(self, *args, **kwargs):
        """Get grid postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}_{}'.format(
            self.cfg['domain'], self.cfg['rcm_model_name'])

        return postfix

    def _get_var_dir_file(self, variable=None, start_date=None, end_date=None):
        """Get variable directory and filename for cordex data.

        :param variable: Package name of variable for which to get
          information. Default is `None`, in which case the first
          variable in :py:attr:`variables` list is taken.
        :param start_date: Simulation start-date.
        :param end_date: Simulation end-date.
        :type variable: str
        :type start_date: str
        :type end_date: str


        returns: Source directory and filename.
        :rtype: tuple of str
        """
        # Take first dates if not given
        start_date = start_date or self.cfg['streams']['start_dates'][0]
        end_date = end_date or self.cfg['streams']['end_dates'][0]

        if variable is None:
            src_var_name, it = None, 0
            while src_var_name is None:
                var_name = list(self.variables)[it]
                src_var_name = self.cfg['variable_names'].get(var_name)
                it += 1
        else:
            src_var_name = self.cfg['variable_names'][variable]

        src_dir = self.med.cfg.get_external_data_directory(self)
        sim_dir = self._get_sim_dir()
        var_dir = os.path.join(src_dir, sim_dir, src_var_name)
        postfix = self.get_postfix(
            start_date=start_date, end_date=end_date)
        var_file = '{}{}.nc'.format(src_var_name, postfix)

        return var_dir, var_file
