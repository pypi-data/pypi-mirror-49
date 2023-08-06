"""GME API."""
import os
import requests
import zipfile
from io import BytesIO
import pandas as pd
import xarray as xr
from ..data_source import DataSourceLoaderBase


class DataSource(DataSourceLoaderBase):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        name = name or 'gme'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, **kwargs):
        """Download GME data-source."""
        src_dir = self.med.cfg.get_external_data_directory(self)

        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)
        for year in years:
            # Download file
            filename = "Anno{}.zip".format(year)
            server_path = os.path.join(self.cfg['host'], filename)
            r = requests.get(server_path)

            # Unzip
            zip_ref = zipfile.ZipFile(BytesIO(r.content))
            zip_ref.extractall(src_dir)
            zip_ref.close()

        # Remove spaces from filenames
        for fn in os.listdir(src_dir):
            src_file = os.path.join(src_dir, fn)
            if os.path.isfile(src_file) & (fn[:4] == 'Anno'):
                os.rename(src_file, os.path.join(src_dir, fn.replace(' ', '')))

    def load(self, **kwargs):
        """Load GME regional demand data at given frequency.

        :returns: Dataset collecting demand for different periods.
        :rtype: dict

        .. note::
          The GME data is available at the
          `GME website <http://www.gestoremercatienergetici.org>`_.
        """
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Read bidding zones
        zones = list(self.med.geo_src.get_zones(self.med.cfg['area']))

        # Read demand from file
        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)
        for year in years:
            try:
                filename = 'Anno{}.xls'.format(year)
                filepath = os.path.join(src_dir, filename)
                demand = pd.read_excel(
                    filepath, sheet_name=self.cfg['sheet_name'])
            except FileNotFoundError:
                filename = 'Anno{}.xlsx'.format(year)
                filepath = os.path.join(src_dir, filename)
                demand = pd.read_excel(
                    filepath, sheet_name=self.cfg['sheet_name'])

            # Set UTC datetime index from 'Europe/Rome' time with DST
            start = pd.to_datetime(str(demand.iloc[0, 0]) +
                                   '{:02d}'.format(demand.iloc[0, 1] - 1),
                                   format='%Y%d%m%H')
            demand.index = pd.date_range(
                start=start, freq='H', periods=demand.shape[0],
                tz='Europe/Rome').tz_convert(None)

            # Select zones and convert to DataArray
            data = xr.DataArray(
                demand.loc[:, zones], dims=('time', 'region'), name='demand')

            # Add array to record
            da = (data.copy() if year == years[0]
                  else xr.concat([da, data], dim='time'))

        if self.med.cfg['frequency'] == 'day':
            # Get cumulated daily demand
            # (use the mean in case there are less than 24 hours)
            da = da.resample(time='D', keep_attrs=True).mean(
                'time', keep_attrs=True) * 24
            da.attrs['units'] = 'MWh/d'
        else:
            da.attrs['units'] = 'MW'

        # Remove the years appearing from conversion to UTC
        first_date = '{}-01-01'.format(years[0])
        last_date = '{}-12-31'.format(years[-1])
        da = da.sel(time=slice(first_date, last_date))
        da['time'].attrs['timezone'] = 'UTC'
        da.name = self.name

        return {'demand': da}

    def get_postfix(self, **kwargs):
        """Get postfix for GSE data-source.

        returns: Postfix.
        rtype: str
        """
        postfix = '_{}'.format(self.med.cfg['frequency'])

        return postfix
