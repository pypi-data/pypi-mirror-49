"""ISTAT API."""
import os
from ..geo import DefaultMaskAPI, DefaultMaskMaker


class DataSource(DefaultMaskAPI, DefaultMaskMaker):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator. Default is `None`.
        :param name: Data source name.
        :param cfg: Data source configuration.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        name = name or 'istat'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def get_url_filename(self, *args, **kwargs):
        """ Get the URL and file name of the geographical data.

        :param cfg: The dictionary with the climate data configuration.
        :type cfg: dict

        :returns: The URL pointing to the geographical data and
          the name of the shapefile.
        :rtype: tuple of str
        """
        postfix = self.cfg['date'] + self.cfg['resolution']
        dir0 = 'Limiti' + postfix
        url = '{}/{}/{}.zip'.format(self.cfg['host'], self.cfg['path'], dir0)
        dir1 = 'Reg' + postfix
        sf_name = os.path.join(dir0, dir1, dir1 + '.shp')

        return url, sf_name
