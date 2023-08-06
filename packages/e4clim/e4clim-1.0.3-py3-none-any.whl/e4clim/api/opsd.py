"""OPSD API."""
import os
import logging
import numpy as np
import pandas as pd
import xarray as xr

#: Logger.
log = logging.getLogger(__name__)


def process(cfg):
    # Process opsd data
    data = process_base(cfg)

    # Write regional demand and generation
    directories = ('demand', 'generation', 'generation')
    for (k, da) in enumerate(data):
        file_dir = os.path.join(cfg['data_dir'], directories[k])
        os.makedirs(file_dir, exist_ok=True)
        fmt = (da.name, 'opsd', cfg['data']
               ['area'], cfg['frequency'])
        filename = '{}_{}_{}_{}.nc'.format(*fmt)
        filepath = os.path.join(file_dir, filename)
        if not self.cfg.get('no_verbose'):
            log.info('Writting regional {} in {}'.format(
                da.name, filepath))
        da.to_netcdf(filepath)

    # # Get capacity factors
    # filename = 'RESCapacity_' + cfg['data']['area'] + '.csv'
    # filepath = os.path.join('input', cfg['data']['area'], filename)
    # dfCap = pd.read_csv(filepath, header=[0, 1], index_col=0)
    # # Solar
    # gen = data[1]
    # cap = xr.DataArray(dfCap['solar'], dims=('time', 'region'))
    # cap.loc[:, 'ITALIA'] = np.nan
    # cap = cap.dropna(dim='region', how='all')
    # (genbc, capbc) = xr.broadcast(gen, cap)
    # CF = gen / cap


def process_base(cfg):
    """ Reads hourly regional load and generation from opsd file
    and return the complete hourly/daily dataset.

    :param cfg: The configuration.
    :type cfg: dict

    :returns: The collected load and generation data.
    :rtype: xarpray.DataArray

    .. todo:: Deal with offshore wind in addition to onshore wind.
    """
    sindex = 'multiindex'
    header = list(range(6))
    skiprows = [6]

    # Read data file
    src_dir = os.path.join(cfg['opsd']['dir'], str(
        cfg['opsd']['version']), cfg['data']['area'])
    filename = 'time_series_{}_{}min_{}.csv'.format(
        cfg['data']['area'], cfg['opsd']['min'], sindex)
    filepath = os.path.join(src_dir, filename)
    if not self.cfg.get('no_verbose'):
        log.info('Reading entso-e data from {}'.format(filepath))
    df = pd.read_csv(filepath, header=header, index_col=0,
                     parse_dates=True, skiprows=skiprows)

    # Select regions
    filename = 'regions_{}.csv'.format(cfg['data']['area'])
    filepath = os.path.join('input', cfg['data']['area'], filename)
    # Read regional information
    regions = pd.read_csv(filepath, index_col=0)['opsd'].values
    df = df[regions]

    # Remove column index levels not used and rename them
    level = np.array(df.columns.names)[2:].tolist()
    df = df.T.reset_index(level=level, drop=True).T
    df.columns = df.columns.remove_unused_levels()
    df = df.columns.set_levels(regions, level='region')

    # Resample
    if cfg['frequency'] == 'day':
        # Get cumulated daily demand (and remove hour)
        df = df.groupby(df.index.date).sum()
        # Center time to adjust to climate data
        df.index = pd.to_datetime(df.index)

    # Convert to DataArray
    ds = xr.DataArray(df, dims=('time', 'regvar')).unstack(
        'regvar').to_dataset('variable')

    # Rename onshore wind to wind
    if 'wind_onshore' in ds:
        ds = ds.rename(wind_onshore='wind')

    data = []
    for var in ds:
        if var not in ds.dims:
            # Select variables
            da = ds[var]

            # Remove missing values
            da = da.where(da > 1.e-6).dropna(dim='time', how='all')

            # Add units and create dataset
            if cfg['frequency'] == 'day':
                da.attrs['units'] = 'MWh/d'
            else:
                da.attrs['units'] = 'MW'

            # Save array to return it
            data += [da]

    return data
