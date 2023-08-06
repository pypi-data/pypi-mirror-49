"""ENTSOE API."""
import os
import logging
import numpy as np
import pandas as pd
import xarray as xr
from entsoe import EntsoePandasClient
from entsoe.mappings import PSRTYPE_MAPPINGS
from ..geo import get_country_code
from ..container import ensure_collection
from ..data_source import DataSourceLoaderBase

#: Logger.
log = logging.getLogger(__name__)


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
        name = name or 'entsoe'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

        self.sampling_conversion = {'P1Y': 'Y', 'PT60M': 'H'}

    def download(self, variables=None, comp_names=None, **kwargs):
        """Download ENTSO-E data from Transparency Platform.

        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :param comp_names: Names of component for which to download data.
          Default is `None`, in which case data is downloaded for
          all mediator components containing this data source.
        :type variables: (collection of) :py:class:`str`
        :type comp_names: :py:class:`list` of :py:class:`str`
        """
        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        if comp_names is None:
            # Load for all mediator components containing this data source
            comp_names = [comp.name for comp in self.med.components.values()
                          if self.name in comp.data_sources]
        else:
            comp_names = ensure_collection(comp_names)

        # Define start and end dates
        start = pd.Timestamp(self.cfg['period_start'], tz=self.cfg['tz'])
        end = pd.Timestamp(self.cfg['period_end'], tz=self.cfg['tz'])
        svar = ', '.join(str(var_name) for var_name in variables)
        if not self.cfg.get('no_verbose'):
            log.info('{} variables from {} to {}:'.format(svar, start, end))

        # Get credentials and start ENTSO-E client
        cred = self.med.cfg.get_credentials(self.name, ['security_token'])
        client = EntsoePandasClient(api_key=cred['security_token'])

        # Get country code
        country_code = get_country_code(
            self.med.cfg['area'], code='alpha-2')

        # Get zones description
        if self.cfg['lookup_bzones']:
            zones_desc = self.med.geo_src.get_zones(self.med.cfg['area'])
            zones_codes = {z: '{}-{}'.format(country_code, z)
                           for z in zones_desc}
        else:
            zones_codes = {self.med.cfg['area']: country_code}

        # Loop over variables
        for var_name in variables:
            # Define query
            src_var_name = self.cfg['variable_names'][var_name]
            if not self.cfg.get('no_verbose'):
                log.info('- {}:'.format(var_name))
            query = getattr(client, 'query_{}'.format(src_var_name))

            # Loop over components
            for comp_name in comp_names:
                src_comp_name = self.cfg['component_names'][comp_name]
                psr_type = [k for k, v in PSRTYPE_MAPPINGS.items()
                            if v == src_comp_name][0]
                if not self.cfg.get('no_verbose'):
                    log.info('-- {} -> {} -> {}:'.format(
                        comp_name, src_comp_name, psr_type))
                # Loop over zones
                without_zones = True
                for zone_name, code in zones_codes.items():
                    if not self.cfg.get('no_verbose'):
                        log.info('--- {}'.format(zone_name))
                    try:
                        # Try with zones
                        df = query(
                            code, start=start, end=end, psr_type=psr_type,
                            lookup_bzones=self.cfg['lookup_bzones'])
                    except TypeError:
                        if without_zones:
                            # Get dataset without zones instead
                            if self.cfg['lookup_bzones']:
                                log.warning(
                                    '{} dataset not zonal: downloading '
                                    'for country instead'.format(var_name))
                            df = query(country_code, start=start, end=end,
                                       psr_type=psr_type)
                            zone_name = self.med.cfg['area']
                            without_zones = False
                        else:
                            # Otherwise break zones loop
                            break

                    # Adjust names
                    df.index.name = 'time'
                    df.columns = [comp_name]

                    # Save locally
                    filepath = self.get_download_filepath(
                        var_name, zone_name, comp_name)
                    df.to_csv(filepath)
        # if self.cfg['download']:
        # else:
        #     log.info('{} data to be fetched and directly loaded: '
        #                  'skipping download'.format(self.name))

    def load(self, variables=None, comp_names=None, **kwargs):
        """Load ENTSO-E time series.

        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :param comp_names: Names of component for which to download data.
          Default is `None`, in which case data is downloaded for
          all mediator components containing this data source.
        :type variables: (collection of) :py:class:`str`
        :type comp_names: :py:class:`list` of :py:class:`str`

        :returns: Time series for each variable and component.
        :rtype: dict
        """
        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        if comp_names is None:
            # Load for all mediator components containing this data source
            comp_names = [comp.name for comp in self.med.components.values()
                          if self.name in comp.data_sources]
        else:
            comp_names = ensure_collection(comp_names)

        # Get country code
        country_code = get_country_code(
            self.med.cfg['area'], code='alpha-2')

        # Get zones description
        if self.cfg['lookup_bzones']:
            zones_desc = self.med.geo_src.get_zones(self.med.cfg['area'])
            zones_codes = {z: '{}-{}'.format(country_code, z)
                           for z in zones_desc}
        else:
            zones_codes = {self.med.cfg['area']: country_code}

        # Loop over datasets
        ds = {}
        for var_name in variables:
            if not self.cfg.get('no_verbose'):
                log.info('- {}:'.format(var_name))
            # Loop over components
            for ic, comp_name in enumerate(self.cfg['component_names']):
                if not self.cfg.get('no_verbose'):
                    log.info('-- {}:'.format(comp_name))
                # Loop over zones
                for ip, (zone_name, code) in enumerate(zones_codes.items()):
                    if not self.cfg.get('no_verbose'):
                        log.info('--- {}'.format(zone_name))
                    # Read downloaded data
                    filepath = self.get_download_filepath(
                        var_name, zone_name, comp_name)
                    df = pd.read_csv(filepath, index_col=0, parse_dates=True)

                    # Convert index timezone to UTC
                    df.index = pd.to_datetime(
                        df.index, utc=True).tz_convert(None)

                    # Convert to DataArray
                    da_zone = xr.DataArray(
                        df, dims=('time', 'component')).expand_dims(
                            'region').assign_coords(region=[zone_name])

                    # Concatenate
                    da_comp = (da_zone if ip == 0 else
                               xr.concat([da_comp, da_zone], dim='region'))

                # Concatenate
                da = (da_comp if ic == 0 else
                      xr.concat([da, da_comp], dim='component'))

            if var_name == 'generation':
                # Set inconsistent values to NaN
                time_slice = slice('2016-10-26T00:00', '2016-11-01T00:00')
                da.loc[{'time': time_slice}] = np.nan

            # Transpose
            ds[var_name] = da.transpose('time', 'component', 'region')

        return ds

    def get_download_filepath(self, variable, zone_name, comp_name):
        """Get downloaded dataset filepath.

        :param variable: Dataset name.
        :param zone_name: Zone or country name.
        :param comp_name: Component name.
        :type variable: str
        :type zone_name: str
        :type comp_name: str

        :returns: Filepath
        :rtype: str
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        src_dir = os.path.join(src_dir, self.med.cfg['area'], variable)
        os.makedirs(src_dir, exist_ok=True)
        filename = '{}_{}_{}_{}{}.csv'.format(
            self.name, variable, zone_name, comp_name,
            self.get_postfix())
        filepath = os.path.join(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get data source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['period_start'], self.cfg['period_end'])

        return postfix
