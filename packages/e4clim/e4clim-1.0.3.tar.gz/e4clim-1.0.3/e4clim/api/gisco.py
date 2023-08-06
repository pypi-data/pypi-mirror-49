"""GISCO API."""
import os
import requests
import logging
from ..geo import DefaultMaskAPI, DefaultMaskMaker

#: Logger.
log = logging.getLogger(__name__)


class DataSource(DefaultMaskMaker, DefaultMaskAPI):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor calling :py:class:`DefaultMaskMaker`'s
        constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        name = name or 'gisco'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def get_url_filename(self, **kwargs):
        """ Get the URL and file name of the geographical data for a given region.

        :returns: The URL pointing to the geographical data and
          the name of the shapefile.
        :rtype: tuple of str
        """
        # Get the list of files
        path = self.cfg['host'] + '/' + self.cfg['path'] + '/'
        url_files = path + 'nuts-{}-files.json'.format(self.cfg['year'])
        n_trials = 0
        while n_trials < self.cfg['max_fetch_trials']:
            try:
                r = requests.get(url_files)
                break
            except requests.exceptions.SSLError as e:
                # Retry
                log.warning(
                    '{} trial to fetch {} file list failed: {}'.format(
                        n_trials + 1, self.namestr(e)))
                n_trials += 1
                continue
        # Verify that last trial succeeded
        if n_trials >= self.cfg['max_fetch_trials']:
            # All trials failed
            log.critical(
                'Fetching failed after {:d} trials'.format(n_trials))
            raise RuntimeError

        if r.status_code != 200:
            raise OSError(url_files)
        # Select the appropriate key
        fmt = (self.cfg['spatial_type'], self.cfg['scale'],
               self.cfg['year'], self.cfg['projection'],
               self.cfg['nuts_level'])
        key = 'NUTS_{}_{}_{}_{}_LEVL_{}.geojson'.format(*fmt)
        # Get the filename
        sf_url = r.json()['geojson'][key]
        url = path + sf_url

        # Remove subdirectories from file name
        sf_name = os.path.normpath(sf_url).split(os.sep)[-1]

        return url, sf_name
