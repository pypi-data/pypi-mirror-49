"""EEA API."""
from ..geo import DefaultMaskAPI, DefaultMaskMaker


class DataSource(DefaultMaskAPI, DefaultMaskMaker):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        name = name or 'eea'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def get_url_filename(self, *args, **kwargs):
        """Get URL and filename of geographical data for a given region.

        :param cfg: Configuration.
        :param sub_region: Secondary region to select. If `None`,
          the whole region is selected. Default is `None`.
        :type cfg: dict
        :type sub_region: str

        :returns: URL pointing to geographical data and name of shapefile.
        :rtype: :py:class:`tuple` of :py:class:`str`
        """
        sub_region = kwargs.get('sub_region', self.med.cfg['area'])

        url = '{}/{}/{}{}'.format(self.cfg['host'], self.cfg['path'],
                                  sub_region.lower(), self.cfg['postfix'])
        sf_name = sub_region.lower()[:2] + '_' + self.cfg['resolution']

        return url, sf_name
