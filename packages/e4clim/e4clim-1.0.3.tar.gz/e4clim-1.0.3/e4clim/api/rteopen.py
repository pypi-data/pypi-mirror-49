"""Download generation data in France from rte opendata portal."""
import os
import logging
import requests
import zipfile
from io import BytesIO
import shapefile
import numpy as np
import pandas as pd
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
        name = name or 'rteopen'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, *args, **kwargs):
        """Download RTE data.

        .. todo:: Add variables management as for ENTSO-E.
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        sformat = 'format=' + self.cfg['format']
        stz = 'timezone=' + self.cfg['timezone']

        # Year and region position in record
        idx_year, idx_reg = 0, 2

        for ds_name, cfg_ds in self.cfg['dataset'].items():
            url = '{}/{}/download?{}&{}'.format(
                self.cfg['host'], ds_name, sformat, stz)
            if not self.cfg.get('no_verbose'):
                log.info('Downloading {} from {}'.format(ds_name, url))
            r = requests.get(url)

            # Extract
            if not self.cfg.get('no_verbose'):
                log.info('Extracting {} in {}'.format(ds_name, src_dir))
            zip_ref = zipfile.ZipFile(BytesIO(r.content))
            zip_ref.extractall(src_dir)
            zip_ref.close()

            # Convert to CSV
            if not self.cfg.get('no_verbose'):
                log.info('Converting to CSV')
            # Read shapefile
            sf = shapefile.Reader(os.path.join(src_dir, ds_name))

            # Get number regions and years
            records = sf.records()
            n_rec = len(records)
            regions = np.unique([records[k][idx_reg] for k in range(n_rec)])
            years = np.unique([records[k][idx_year] for k in range(n_rec)])

            # Create the dictionary of DataFrames
            d = {}
            for field in self.cfg['field_indices']:
                d[field] = pd.DataFrame(index=years, columns=regions)

            # Add all records to the DataFrames
            for record in sf.iterRecords():
                # For each field
                for field, df in d.items():
                    df.loc[record[0], record[2]] = record[
                        self.cfg['field_indices'][field]]

            # Save DataFrames as CSV
            for field, df in d.items():
                filename = ds_name + '_' + field + '.csv'
                filepath = os.path.join(src_dir, filename)
                if not self.cfg.get('no_verbose'):
                    log.info('Writing field {} to {}'.format(field, filepath))
                df.to_csv(filepath)

    def load(self, **kwargs):
        """Load RTE data.

        .. todo:: Add variables management as for ENTSO-E.
        """
        # Get configuration file to use and import it
        src_dir = self.cfg['dir']

        ds_name_gen = 'prod_region_filiere'
        ds_name_cap = 'parc_region_annuel_production_filiere'
        ds_name_cf = 'capacity_factors_by_branch'

        # Read generation and capacity records for each fields
        d = {}
        for field in self.cfg['field_indices']:
            filename = ds_name_gen + '_' + field + '.csv'
            df_gen = pd.read_csv(os.path.join(
                src_dir, filename), index_col=0)
            filename = ds_name_cap + '_' + field + '.csv'
            df_cap = pd.read_csv(os.path.join(
                src_dir, filename), index_col=0)

            # Convert generation units from GWh/y to MWh/h
            df_gen = df_gen * 1000 / (365 * 24)

            # Get capacity factors
            df_cf = df_gen / df_cap

            # Make sure the index is as type string and not int
            df_cf.index = df_cf.index.astype(str)

            # Save the capacity factors
            filename = ds_name_cf + '_' + field + '.csv'
            filepath = os.path.join(src_dir, filename)
            if not self.cfg.get('no_verbose'):
                log.info('Writing {} for {} field {} to {}'.format(
                    ds_name_cf, field, filepath))
            df_cf.to_csv(filepath)

            # Keep DataFrame in dictionary
            d[field] = df_cf
