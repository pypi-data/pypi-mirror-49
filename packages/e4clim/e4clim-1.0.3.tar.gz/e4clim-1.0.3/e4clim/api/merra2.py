"""MERRA-2 API."""
import os
import logging
from collections import OrderedDict
import requests
import netCDF4 as nc
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
        name = name or 'merra2'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

        # Frequency code
        self.freq_code = {'hour': '1', 'day': 'D'}

        # If lat_range and lon_range are not given, they will
        # be computed from mask regions total bounds when needed
        self.lat_range = self.cfg.get('lat_range')
        self.lon_range = self.cfg.get('lon_range')

        # Server parent directory
        self.srv_parent_dir = '{}/opendap/hyrax/{}/{}{}{}{}{}'.format(
            self.cfg['host'], self.name.upper(),
            self.cfg['data_name'], self.cfg['time_description'],
            self.freq_code[self.cfg['frequency']],
            self.cfg['horizontal_resolution'],
            self.cfg['vertical_location'].upper())

    def download(self, variables=None, **kwargs):
        """Download merra2 data and save it to disk.

        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :type variables: (collection of) :py:class:`str`
        """
        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        # Loop over days
        date_range = pd.date_range(
            start=self.cfg['start_date'], end=self.cfg['end_date'],
            freq='D', closed='left')
        for date in date_range:
            for var_name in variables:
                # Download data for date and variable
                self._download_date_variable(
                    date, var_name, download=True, **kwargs)

    def load(self, transform=None, variables=None, **kwargs):
        """Collect all required variables from the MERRA-2 re-analysis.

        :param transform: A function or a composee of functions
          to apply to the datasets.
          These functions should take as arguments a dataset and a
          :py:class:`.data_source.DataSourceBase` data source.
        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :type transform: :py:class:`func` or
          :py:class:`.data_source.Composer`
        :type variables: (collection of) :py:class:`str`

        :returns: A dataset collecting all the variables and periods.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        # Loop over days
        date_range = pd.date_range(
            start=self.cfg['start_date'], end=self.cfg['end_date'],
            freq='D', closed='left')
        ds = None
        for date in date_range:
            # Collect all variables from all groups
            ds_per = xr.Dataset()
            if not self.cfg.get('no_verbose'):
                log.info('Reading data for {}'.format(
                    date.date()))
            for var_name in variables:
                src_var_name = self.cfg['variable_names'].get(var_name)

                # Read data for date and variable
                ds_gp = self._download_date_variable(
                    date, var_name, download=False, **kwargs)
                if ds_gp is None:
                    continue

                # Add height
                self._add_height(ds_gp)

                # Rename variable
                ds_gp = ds_gp.rename(**{src_var_name: var_name})

                # Merge group
                ds_per = ds_per.merge(ds_gp)
                ds_gp.close()

            # Remove conflicting attributes to avoid
            # AttributeError: NetCDF: String match to name in use
            try:
                del ds_per.time.attrs['CLASS']
                del ds_per.time.attrs['NAME']
            except KeyError:
                pass

            # Apply functions to the dataset if given
            if transform:
                kwargs.update({'ds': ds_per, 'data_src': self})
                ds_per = transform(**kwargs)

            # Create or add period
            ds = ds_per if ds is None else xr.concat([ds, ds_per], dim='time')

        # Change hour interval representation convention from center to left
        t = ds.indexes['time']
        new_index = pd.to_datetime(
            {'year': t.year, 'month': t.month, 'day': t.day, 'hour': t.hour})
        ds = ds.reindex(time=new_index, method='bfill')
        ds.time.encoding['units'] = "hours since 1980-01-01T00:00:00"

        return ds

    def get_postfix(self, start_date=None, end_date=None, **kwargs):
        """Get postfix for the MERRA-2 data.

        :param start_date: Simulation start-date. Default is `None`, in which
          case the first date of `self.cfg['streams']['start_dates']` is used.
        :param end_date: Simulation end-date. Default is `None`, in which case
          the first date of `self.cfg['streams']['end_dates']` is used.
        :type start_date: str
        :type end_date: str

        :returns: Postfix.
        :rtype: str
        """
        start_date = start_date or self.cfg['start_date']
        end_date = end_date or self.cfg['end_date']

        # Get paths
        postfix = '_{}_{}-{}'.format(self.cfg['frequency'],
                                     start_date, end_date)

        return postfix

    def get_index_lon(self, lon):
        """Get grid index corresponding to longitude.

        :param lon: Longitude.
        :type lon: :py:class:`float`, array_like

        :returns: Longitude grid-index.
        :rtype: :py:class:`int`, :py:class:`numpy.array`
        """
        ilon = (lon + 180.) / self.cfg['delta_lon'] + 1
        try:
            ilon = int(ilon + 0.1)
        except TypeError:
            ilon = (np.array(ilon) + 0.1).astype(int)

        return ilon

    def get_index_lat(self, lat):
        """Get grid index corresponding to latitude.

        :param lat: Latitude.
        :type lat: :py:class:`float`, array_like

        :returns: Latitude grid-index.
        :rtype: :py:class:`int`, :py:class:`numpy.array`
        """
        ilat = (lat + 90.) / self.cfg['delta_lat'] + 1
        try:
            ilat = int(ilat + 0.1)
        except TypeError:
            ilat = (np.array(ilat) + 0.1).astype(int)

        return ilat

    def get_lat_lon_range(self):
        """Get latitude and longitude ranges for filenames.

        :returns: Latitude and longitude ranges.
        :rtype: :py:class:`tuple` of :py:class:`str`
        """
        # Get total bounds in geoid system
        lon_min, lat_min, lon_max, lat_max = (
            self.med.geo_src.get_total_bounds(epsg=4326))

        # Convert bounds to grid indices
        ilon_min = self.get_index_lon(lon_min)
        ilon_max = self.get_index_lon(lon_max + 1)
        ilat_min = self.get_index_lat(lat_min)
        ilat_max = self.get_index_lat(lat_max + 1)

        # Get grid string
        lon_rng = '[{:d}:{:d}]'.format(ilon_min, ilon_max)
        lat_rng = '[{:d}:{:d}]'.format(ilat_min, ilat_max)

        return lat_rng, lon_rng

    def get_url_file_dir_file(self, var_name=None, date=None):
        """Get variable URL, directory and filename for MERRA-2 data.

        :param var_name: Variable name. Default is `None`.
        :param date: Date for which to return paths.
          If `None`, use `'start_date'` value of data source configuration.
          Default is `None`.
        :type var_name: str

        returns: Source URL, directory and filename.
        :rtype: :py:class:`tuple` of :py:class:`str`
        """
        if (not self.lat_range) or (not self.lon_range):
            self.lat_range, self.lon_range = self.get_lat_lon_range()
        domain = '[0:23]' + self.lat_range + self.lon_range
        time_range = ('' if self.cfg['space'] == '2d'
                      else self.cfg['time_range'])
        grid_list = 'time{},lat{},lon{}'.format(
            time_range, self.lat_range, self.lon_range)

        # Get data source directory
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Get given date or start date
        date = pd.Timestamp(date or self.cfg['start_date'])

        # Get runid of stream containg date
        for (stream, cfg_stream) in self.cfg['streams'].items():
            ssd = pd.Timestamp(cfg_stream['start_date'])
            sed = pd.Timestamp(cfg_stream['end_date'])
            if (date >= ssd) & (date < sed):
                break
        runid = '{}{}'.format(stream, self.cfg['version'])
        freq = 'tavg' + self.freq_code[self.cfg['frequency']]
        prefix0 = '{}_{}.{}_{}'.format(
            self.name.upper(), runid, freq, self.cfg['space'])

        if var_name is None:
            # Take first variable in a group
            group_name = None
            it = 0
            while group_name is None:
                var_name = list(self.variables)[it]
                group_name = self.cfg['group_names'].get(var_name)
                it += 1
        else:
            # Try to get group of variable
            group_name = self.cfg['group_names'].get(var_name)
        src_var_name = self.cfg['variable_names'].get(var_name)

        # Make local directories
        file_dir = os.path.join(src_dir, group_name)
        os.makedirs(file_dir, exist_ok=True)

        HV = '{}{}'.format(self.cfg['horizontal_resolution'],
                           self.cfg['vertical_location'])
        prefix = '{}_{}_{}.{}.{}'.format(
            prefix0, group_name, HV, date.strftime('%Y%m%d'),
            self.cfg['format'])
        postfix = '{}{},{}'.format(src_var_name, domain, grid_list)
        filename = '{}.nc?{}'.format(prefix, postfix)

        srv_dir = '{}{}.{}'.format(
            self.srv_parent_dir, group_name.upper(), self.cfg['geos5_version'])
        url = '{}/{:04d}/{:02d}/{}'.format(
            srv_dir, date.year, date.month, filename)

        return url, file_dir, filename

    def get_grid(self, *args, **kwargs):
        """Get grid used to make masks.

        :returns: Dataset coordinates.
        :rtype: :py:class: `tuple` of pairs of :py:class: `str`
          and :py:class: `numpy.array`
        """
        # Get paths
        url, file_dir, filename = self.get_url_file_dir_file()

        # Read coords
        filepath = os.path.join(file_dir, filename)
        if not self.cfg.get('no_verbose'):
            log.info('Reading coordinates from {}'.format(filepath))
        ds = xr.open_dataset(filepath)

        coords = OrderedDict({
            'lat': ds['lat'].copy(deep=True).values,
            'lon': ds['lon'].copy(deep=True).values})
        ds.close()

        return coords

    def get_grid_postfix(self, *args, **kwargs):
        """Grid postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}{}'.format(self.cfg['horizontal_resolution'],
                                 self.cfg['vertical_location'])

        return postfix

    def _download_request(self, url):
        """Download data over HTTP - OPeNDAP.

        :param url: OPeNDAP URL.
        :type url: str

        :returns: Dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Request data
        r = requests.get(url)

        # Convert bytes to netCDF4.Dataset
        ds_nc = nc.Dataset(filename='dum.nc', memory=r.content)

        # Convert netCDF4.Dataset to xarray.Dataset
        ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds_nc))

        return ds

    def _download_date_variable(
            self, date, var_name, download=False, **kwargs):
        """Download data for given date and variable.

        :param date: Date.
        :param var_name: Variable name.
        :param download: Whether to direclty download data, or to try to
          read it from disk first. Default is `False`, in which case
          an attempt is made to read first.
        :type date: datetime
        :type var_name: str
        :type download: bool
        """
        # Get group name for variable
        group_name = self.cfg['group_names'].get(var_name)
        src_var_name = self.cfg['variable_names'].get(var_name)
        if (src_var_name is None) or (group_name is None):
            log.warning(
                "{} variable not in 'variable_names' of {} "
                "configuration-file: skipping".format(
                    var_name, self.name))
            return

        # Get paths
        url, file_dir, filename = self.get_url_file_dir_file(
            var_name=var_name, date=date)

        # Fetch data
        n_trials = 0
        while n_trials < self.cfg['max_fetch_trials']:
            try:
                if (not download) and (n_trials == 0):
                    # Read previously downloaded data
                    filepath = os.path.join(file_dir, filename)
                    ds = xr.open_dataset(filepath)
                else:
                    # Try to fetch
                    if not self.cfg.get('no_verbose'):
                        log.info('Fetching {} group from {}'.format(
                            group_name, url))
                        ds = self._download_request(url)

                # Check quality
                if self.cfg.get('check_quality'):
                    _quality_check(ds)

                # Everything went well -> leave trials loop
                break
            except (OSError, RuntimeError,
                    AttributeError, ValueError) as e:
                # Retry
                log.warning(
                    'Fetching trial {:d} failed: {}'.format(
                        n_trials + 1, str(e)))
                n_trials += 1
                continue

        # Verify that last trial succeeded
        if n_trials >= self.cfg['max_fetch_trials']:
            # All trials failed
            log.critical('Fetching failed after {:d} '
                         'trials. '.format(n_trials))
            raise RuntimeError
        elif download or (n_trials > 0):
            # Write data
            filepath = os.path.join(file_dir, filename)
            if not self.cfg.get('no_verbose'):
                log.info('Writing {} group to {}'.format(
                    group_name, filepath))
            ds.to_netcdf(filepath)

        return ds

    def _add_height(self, ds):
        """Add or rename `'height'` variable to dataset attributes.

        :param ds: Dataset.
        :type ds: :py:class:`xarray.Dataset`
        """
        for svn in ds.data_vars:
            var = ds[svn]
            if self.cfg['height'] not in var.attrs:
                # Add height as attribute
                if self.cfg['height'] in ds:
                    var.attrs['height'] = float(
                        ds[self.cfg['height']])
                elif self.cfg['height'] in ds.coords:
                    var.attrs['height'] = float(
                        ds.coords[self.cfg['height']])
                else:
                    # Get height from wind name or assume 2m height
                    var.attrs['height'] = (
                        float(svn[1:svn.find('M')])
                        if svn[0] in ['U', 'V'] else 2.)
            else:
                # Rename
                var.attrs['height'] = var.attrs[self.cfg['height']]


def _quality_check(ds):
    """Check integrity of downloaded dataset. If dataset is invalid,
    `ValueError` is raised.

    :param ds: Dataset to check.
    :type ds: :py:class:`xarray.Dataset`
    """
    # Time index
    if (ds.indexes['time'].year == 1970).any():
        raise ValueError

    # NaN and Infinite values
    for da in ds.values():
        if da.isnull().any() or (da > 1e10).any():
            raise ValueError
