"""GSE API."""
import logging
from pkg_resources import resource_stream
import numpy as np
import pandas as pd
import xarray as xr
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
        name = name or 'gse'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, *args, **kwargs):
        """Convenience function to warn that GME data is not downloaded
        but loaded from package data.
        """
        log.warning('{} is not to be downloaded. It is instead directly '
                    'loaded from the package data.'.format(self.name))

    def load(self, variables=None, comp_names=None, **kwargs):
        """Load GSE zonal electricity data.

        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are loaded.
        :param comp_names: Names of component for which to load data.
          Default is `None`, in which case data is loaded for
          all mediator components containing this data source.
        :type variables: (collection of) :py:class:`str`
        :type comp_names: :py:class:`list` of :py:class:`str`

        :returns: Dataset.
        :rtype: dict

        .. note:: Data was processed from data sheets copied
          from GSE reports with :py:meth:`preprocess_gse_reports`.
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

        # Get subset of zones
        zones = list(self.med.geo_src.get_zones(self.med.cfg['area']))

        ds = {}
        for variable in variables:
            # Read preprocessed GSE report for this variable
            resource_name = self.get_download_resource_name(variable)
            with resource_stream(__name__, resource_name) as f:
                da = xr.open_dataarray(f).sel(
                    component=comp_names, region=zones).copy(deep=True)
            ds[variable] = da

        return ds

    def get_download_resource_name(self, variable):
        """Get package resource name for data copied from GSE reports.

        :param variable: Variable name.
        :type variable: str

        :returns: Resource name.
        :rtype: str
        """
        filename = '{}_{}_zone_{}.nc'.format(
            variable, self.med.cfg['area'], self.name)
        resource_name = '../data/{}/{}/{}'.format(
            self.med.cfg['area'], self.name, filename)

        return resource_name

    def preprocess_gse_reports(self, *args, variable='capacity_factor',
                               **kwargs):
        """Load GSE zonal electricity data.

        :param variable: Dataset name. Default is `'capacity_factor'`.
        :type variable: str

        :returns: Dataset collecting the capacity factors, capacity and
          generation.
        :rtype: :py:class:`xarray.Dataset`
        """
        years = np.arange(2008, 2017)
        component = ['hydro', 'wind', 'pv']
        values = {'capacity': [1, len(component) * 2, 2],
                  'generation': [0, len(component), 1]}
        units = {'capacity': ['MW', 1.], 'generation': ['MWh', 1.e3],
                 'capacity_factor': ['', 1.]}
        special = ["'", " "]

        # Read the bidding zones
        zones_desc = self.med.geo_src.get_zones(self.med.cfg['area'])
        zone_regs = {k: v['regions'] for k, v in zones_desc.items()}

        # Dictionary of dataframes
        ddf = {}

        # Get yearly data
        for df_name in ['capacity', 'generation']:
            if variable in [df_name, 'capacity_factor']:
                vls = values[df_name]
                # Read data
                resource_name = self.get_download_resource_name(df_name)
                if not self.cfg.get('no_verbose'):
                    log.info('Reading package resource {}'.format(
                        resource_name))
                with resource_stream(__name__, resource_name) as f:
                    content = f.readlines()

                for (y, year) in enumerate(years):
                    line = content[y]
                    data_year = {}
                    k = 0
                    while k < len(line):
                        # Get the name of the first region
                        k0 = k
                        while (line[k].isalpha() or line[k] in special):
                            k += 1
                        reg_name = line[k0:k].strip()

                        # Save regional values
                        k0 = k
                        while ((k < len(line)) and
                               (not line[k % len(line)].isalpha())):
                            k += 1
                        data_year[reg_name] = np.array(
                            line[k0:k].split(), dtype=float)[
                                vls[0]:vls[1]:vls[2]]

                    # Make the column multi-index the first year
                    if y == 0:
                        columns = pd.MultiIndex.from_product(
                            [component, data_year.keys()],
                            names=['component', 'region'])
                        df = pd.DataFrame(
                            index=years, columns=columns, dtype=float)

                    # Save the yearly data
                    df.loc[year] = pd.DataFrame(
                        data_year, index=component).stack()

                # Remove Italy
                df.loc[:, (slice(None), 'ITALIA')] = np.nan
                df = df.dropna(axis='columns', how='all')

                # Group by zones
                for (zone, regions) in zone_regs.items():
                    for reg in regions:
                        df = df.rename({reg: zone}, axis=1)
                df = df.groupby(axis=1, level=['region', 'component']
                                ).sum().swaplevel(0, 1, axis=1)
                df.columns = df.columns.remove_unused_levels()

                if df_name == 'capacity':
                    # Get capacity at middle of year
                    df_mid = df[1:]
                    df_mid.values[:] = (df[1:].values + df[:-1].values) / 2
                    df = df_mid
                elif df_name == 'generation':
                    df = df[1:]

                # Convert units and add to dictionary
                ddf[df_name] = df * units[df_name][1]

        # Estimate capacity at the middle of the year
        # to compute the capacity factors
        if variable == 'capacity_factor':
            # Get capacity factors (%) and write
            ddf['capacity_factor'] = (
                ddf['generation'] / (ddf['capacity'] * 24 * 365))

        # Define time index
        time = pd.to_datetime(
            {'year': ddf[list(ddf)[0]].index.values.astype(str),
             'month': 12, 'day': 31})
        time = pd.DatetimeIndex(time, freq='A-DEC')

        # Return dataset
        da = xr.DataArray(
            ddf[variable], dims=('time', 'comp_reg'), name=variable,
            attrs={'units': units[variable][0]}).unstack('comp_reg')
        da['time'] = time
        comp_names = {comp_src_name: comp_name for comp_name, comp_src_name
                      in self.cfg['component_names'].items()}
        ds = da.to_dataset(dim='component').rename(**comp_names)
        if variable == 'capacity':
            ds.attrs['note'] = (
                'The value the 31st of December of a given year corresponds '
                'to the mean capacity between this year and the previous one.')

        return ds
