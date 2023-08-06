"""RTE API."""
import os
import logging
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
import numpy as np
import pandas as pd
import xarray as xr
from ..data_source import DataSourceLoaderBase
from ..container import ensure_collection

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
        name = name or 'rte'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, variables=None, comp_names=None, **kwargs):
        """Download RTE data.

        :param variables: Names of variables to download. Default is `None`,
          in which case all variables in :py:attr`variables` are downloaded.
        :param comp_names: Names of component for which to download data.
          Default is `None`, in which case data is downloaded for
          all mediator components containing this data source.
        :type variables: (collection of) :py:class:`str`
        :type comp_names: :py:class:`list` of :py:class:`str`
        """
        timezone = self.cfg['timezone']
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Get list of variables from argument or from attribute
        variables = (ensure_collection(variables, set)
                     if variables is not None else self.variables)

        if comp_names is None:
            # Load for all mediator components containing this data source
            comp_names = [comp.name for comp in self.med.components.values()
                          if self.name in comp.data_sources]
        else:
            comp_names = ensure_collection(comp_names)

        # Get credentials
        cred = self.med.cfg.get_credentials(
            self.name, ['client_id', 'client_secret'])

        # Access OAuth2 authentification token
        token_url = '{}/token/oauth/'.format(self.cfg['host'])
        auth = HTTPBasicAuth(cred['client_id'], cred['client_secret'])
        client = BackendApplicationClient(client_id=cred['client_id'])
        oauth = OAuth2Session(client=client)
        _ = oauth.fetch_token(token_url=token_url, auth=auth)

        # Loop over variables
        for var_name in variables:
            dep_vars = self.cfg['dependency'][var_name]
            for ds_name in dep_vars:
                cfg_ds = self.cfg['dataset'][ds_name]
                ds_sub_name = cfg_ds['structure']
                start_date = pd.Timestamp(
                    cfg_ds['start_date'], tz=timezone)
                end_date = pd.Timestamp(
                    cfg_ds['end_date']).tz_localize(start_date.tz)
                if not self.cfg.get('no_verbose'):
                    log.info('Downloading dataset {} from {}'.format(
                        ds_sub_name, self.name))

                # Get base URL
                url_base = '{}/open_api/{}/{}/{}'.format(
                    self.cfg['host'], ds_name, self.cfg['version'],
                    ds_sub_name)

                for c in comp_names:
                    comp_name = self.cfg['component_names'][c]
                    if not self.cfg.get('no_verbose'):
                        log.info('Processing variable {}'.format(
                            comp_name))

                    # Make several requests if the limit
                    # on the number of days is exceeded
                    first_record = True
                    rec = pd.Timedelta(cfg_ds['max_record_length'], unit='D')
                    start_date_record = start_date
                    end_date_record = start_date
                    while end_date_record < end_date:
                        end_date_record = pd.Timestamp(
                            (start_date_record + rec).date(), tz=timezone)
                        end_date_record = np.min([end_date_record, end_date])

                        if not self.cfg.get('no_verbose'):
                            log.info('From {} to {}'.format(
                                start_date_record, end_date_record))

                        # Make GET request
                        sstart = start_date_record.strftime('%Y-%m-%dT%H:%M:%S%z')
                        sstart = sstart[:-2] + ':' + sstart[-2:]
                        send = end_date_record.strftime('%Y-%m-%dT%H:%M:%S%z')
                        send = send[:-2] + ':' + send[-2:]
                    
                        # Parse JSON data
                        url = ('{}?start_date={}&end_date={}'
                               '&production_type={}'.format(
                                   url_base, sstart, send, comp_name))
                        r = oauth.get(url)
                        raw_data = r.json()[ds_sub_name]

                        # Some datasets have a 'values' key, others not
                        if 'values' in raw_data:
                            raw_data = raw_data['values']

                        # Get the key of the production type
                        # (it should have 'type' in its key)
                        type_key = np.array(list(raw_data[0]))[['type' in list(
                            raw_data[0])[i] for i in range(len(raw_data[0]))]][0]
                        production_type = [raw_data[k][type_key]
                                           for k in range(len(raw_data))]

                        # Get variable
                        count = production_type.count(comp_name)
                        updated_date = []
                        if count > 0:
                            if count > 1:
                                values = []
                                start_date = []
                                i0 = 0
                                for i in range(count):
                                    idx = production_type[i0:].index(
                                        comp_name)
                                    values.append(raw_data[i0 + idx]['value'])
                                    start_date.append(
                                        raw_data[i0 + idx]['start_date'])
                                    # Add update date if it exists
                                    if 'updated_date' in raw_data[i0 + idx]:
                                        updated_date.append(
                                            raw_data[i0 + idx]['updated_date'])
                                    i0 += idx + 1
                            else:
                                data = raw_data[production_type.index(
                                    comp_name)]['values']
                                start_date = [pd.Timestamp(
                                    data[t]['start_date']).tz_convert(None)
                                              for t in range(len(data))]
                                values = [data[t]['value']
                                          for t in range(len(data))]

                            # Create the dataset for that variable
                            isort = np.argsort(start_date)
                            index = pd.DatetimeIndex(start_date)[isort]
                            coords = [('time', index)]
                            attrs = {'units': cfg_ds['units']}
                            da_var = xr.DataArray(
                                np.expand_dims(values, 1)[
                                    isort], coords=coords,
                                name=ds_sub_name, attrs=attrs)
                            ds_rec = da_var.to_dataset()

                            # Add updated_date if it exists
                            if len(updated_date) > 0:
                                updated_date = pd.DatetimeIndex(
                                    updated_date)[isort]
                                vals = np.expand_dims(updated_date, 1)
                                da_up = xr.DataArray(vals, coords=coords,
                                                     name='updated_date')
                                ds_rec = ds_rec.assign(
                                    **{'updated_date': da_up})

                            # Process missing values
                            da_var = ds_rec[ds_sub_name]
                            na, nt = int(da_var.isnull().sum()
                                         ), da_var.shape[0]
                            if na > 0:
                                if self.cfg['fillna']:
                                    # Fill NaNs
                                    if not self.cfg.get('no_verbose'):
                                        log.info(
                                            '    Filling {} NaN value(s) out '
                                            'of {}'.format(na, nt))
                                    da_var.interpolate_na(
                                        method=self.cfg['fillMethod'],
                                        dim='time')
                                else:
                                    if not self.cfg.get('no_verbose'):
                                        log.info(
                                            'Keeping {} value(s) out of '
                                            '{}'.format(na, nt))

                        else:
                            if not self.cfg.get('no_verbose'):
                                log.info('{} absent'.format(comp_name))

                        # Record record
                        if first_record:
                            ds = ds_rec
                            first_record = False
                        else:
                            # Add record to data frame
                            ds = ds.merge(ds_rec)
                        start_date_record = end_date_record

                    # Save locally
                    ds.time.attrs['timezone'] = 'UTC'
                    filepath = self.get_download_filepath(
                        comp_name, ds_sub_name, cfg_ds, **kwargs)
                    ds.to_netcdf(filepath)

    def load(self, variables=None, comp_names=None, **kwargs):
        """Load RTE data.

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

        # Loop over datasets
        ds = {}
        # Loop over components
        for ic, comp_name in enumerate(self.cfg['component_names']):
            if not self.cfg.get('no_verbose'):
                log.info('-- {}:'.format(comp_name))
            for var_name in variables:
                if not self.cfg.get('no_verbose'):
                    log.info('- {}:'.format(var_name))
                dep_vars = self.cfg['dependency'][var_name]
                ds_dep = {}
                for ds_name in dep_vars:
                    cfg_ds = self.cfg['dataset'][ds_name]
                    ds_sub_name = cfg_ds['structure']

                    filepath = self.get_download_filepath(
                        comp_name, ds_sub_name, cfg_ds, **kwargs)
                    ds_dep[ds_sub_name] = xr.open_dataset(
                        filepath)[ds_sub_name]

        # Read capacities
        ds_name = 'generation_installed_capacities'
        ds_sub_name = 'capacities_per_production_type'
        cfg_ds_sub = self.cfg['dataset'][ds_name][ds_sub_name]
        fmt = (ds_sub_name, self.name, self.cfg['area'],
               cfg_ds_sub['frequency'], cfg_ds_sub['start_date'],
               cfg_ds_sub['end_date'])
        filename = '{}_{}_{}_{}_{}_{}.nc'.format(*fmt)
        filepath = os.path.join(src_dir, filename)
        ds_cap = xr.open_dataset(filepath)
        da_cap_yearly = ds_cap[ds_sub_name]
        # Broadcast yearly capacities against hourly generation
        da_cap = da_cap_yearly.resample(time='1H').asfreq().reindex(
            {'time': da_gen.time}).ffill('time')

        # Compute capacity factors
        cf = da_gen / da_cap

        # Save capacity factors

    def get_download_filepath(self, comp_name, ds_sub_name, cfg_ds, **kwargs):
        """Get downloaded dataset filepath.

        :param comp_name: Component name.
        :param ds_sub_name: Dataset detailed name.
        :param cfg_ds: Dataset configuration.
        :type comp_name: str
        :type ds_sub_name: str
        :type cfg_ds: dict

        :returns: Filepath.
        :rtype: str
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        filename = '{}_{}_{}_{}_{}_{}-{}.nc'.format(
            self.name, self.med.cfg['area'], ds_sub_name, comp_name,
            cfg_ds['frequency'], cfg_ds['start_date'],
            cfg_ds['end_date'])
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
