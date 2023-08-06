"""Database of Global Administrative Areas (GADM) API."""
from ..geo import DefaultMaskAPI, DefaultMaskMaker, get_country_code


class DataSource(DefaultMaskMaker, DefaultMaskAPI):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        name = name or 'gadm'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def get_url_filename(self, **kwargs):
        """Get the URL and file name of the geographical data for a given region.

        :returns: URL pointing to the geographical data and
          the name of the shapefile.
        :rtype: :py:class:`tuple` of :py:class:`str`
        """
        # Get the country code
        country_code = get_country_code(self.med.cfg['area'], code='alpha-3')
        # Get the URL
        fmt = (self.cfg['host'], self.cfg['path'], self.name.lower(),
               self.cfg['version'], self.cfg['format'])
        path = '{}/{}/{}{}/{}/'.format(*fmt)
        fmt = (self.name.lower(), self.cfg['version'].replace('.', ''),
               country_code)
        prefix = '{}{}_{}'.format(*fmt)
        url = path + prefix + '_' + self.cfg['format'] + '.zip'
        sf_name = prefix + '_' + str(self.cfg['level']) + '.shp'
        self.cfg['child_column'] = '{}_{}'.format(
            self.cfg['child_column_prefix'], str(self.cfg['level']))

        return url, sf_name
