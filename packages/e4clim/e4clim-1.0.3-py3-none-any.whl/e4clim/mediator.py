"""Mediator-related definitions."""
import os
import collections
import logging
from warnings import warn
from .config import Config, load_config
from .component import Component, import_module_from_cfg
from .data_source import MultiDataSource
from .container import Container, ensure_collection
from . import __name__ as pkg_name

#: Logger.
log = logging.getLogger(__name__)


class Mediator(Container, collections.MutableMapping):
    """Models mediator."""

    def __init__(self, cfg):
        """Constructor setting configuration and task manager.

        :param cfg: Configuration or a file path from which to read
          configuration.
        :type cfg: :py:class:`dict` or :py:obj:`str`
        """
        # Load configuration
        loaded_cfg = Config(cfg) if type(cfg) is str else cfg

        # Initialize as container
        super(Mediator, self).__init__(self, 'mediator', cfg=loaded_cfg)

        # Set-up logger
        _init_logger(self.cfg)

        if not self.cfg.get('no_verbose'):
            log.info('*** INITIALIZING MEDIATOR ***')

        #: Data-sources mapping.
        self.data_sources = {}

        #: Geographic configuration.
        self.geo_cfg = None
        #: Geographic data-source configuration.
        self.geo_src = None
        # Inject geography in mediator as data source
        self._init_geo()

        # Inject all components in mediator
        if not self.cfg.get('no_verbose'):
            log.info('Injecting {} components to mediator'.format(
                ', '.join(self.cfg['components'].keys())))
        #: Components mapping.
        self.components = {
            comp_name: Component(self, comp_name, out_var_names=var_names)
            for comp_name, var_names in self.cfg['components'].items()}

        # Add components and geographic data-source as children
        self.update_children(self.components)
        self.update_children({self.geo_src.name: self.geo_src})

        # Gridded data-sources list.
        self.gridded_sources = []
        for data_src in self.data_sources.values():
            if data_src.gridded:
                self.gridded_sources.append(data_src)

        #: Optimizer.
        self.optimizer = None
        # Inject optimizer
        self._init_optimizer()

    def add_data_source(self, src_vars, parent=None, **kwargs):
        """ Add single or multiple data source depending on whether
        :py:obj:`src_dict` has keys.

        :param src_vars: Mapping with multiple (source name, variables list)
          (key, value) pairs, sequence of source names, source name.
        :param parent: Container for which to load the source.
          Default is `None`.
        :type src_vars: Mutable mapping, collection or string.
        :type container: :py:class:`.container.Container`

        :returns: Data source.
        :rtype: :py:class:`.data_source.DataSourceBase`

        .. seealso:: :py:meth:`.component.OutputVariable.add_data_source`
        """
        if ((not isinstance(src_vars, str)) and
            isinstance(src_vars, collections.Collection) and
                (len(src_vars) > 1)):
            data_src = self.med.add_multi_data_source(
                src_vars, parent=parent, **kwargs)
        else:
            if isinstance(src_vars, collections.MutableMapping):
                src_name, variables = src_vars.popitem()
            else:
                # Try to get variables from keyword arguments,
                # otherwise, leave None
                variables = kwargs.pop('variables', None)
                try:
                    # Try to unpack length-1 collection
                    src_name = str(*src_vars)
                except TypeError:
                    # Scalar object
                    src_name = str(src_vars)
            data_src = self.med.add_single_data_source(
                src_name, variables=variables, parent=parent, **kwargs)

        return data_src

    def add_single_data_source(self, name, variables=None, parent=None,
                               **kwargs):
        """Initialize a data source, inject to mediator,
        and return it as well.

        :param name: Data source name.
        :param variables: Data source variables. Default is `None`,
          in which case variables should be defined after construction
          by data source or by user.
        :param parent: Container for which to add data source.
          Default is `None`.
        :type name: str
        :type variables: (collection of) :py:class:`str`
        :type parent: :py:class:`.container.Container`

        :returns: (Multiple) data source.
        :rtype: :py:class:`.data_source.DataSourceBase`

        .. seealso:: :py:meth:`add_data_source`
        """
        # Verify that data source not already added by other containers
        if name not in self.data_sources:
            # Add data source configuration
            cfg_src = load_config(self.cfg, name, parent)

            if cfg_src is not None:
                # Import data source module
                mod = import_module_from_cfg(cfg_src, name=name)

                # Create data source and inject it to mediator
                self.data_sources[name] = mod.DataSource(
                    self, name, cfg=cfg_src, variables=variables, **kwargs)

                if not self.cfg.get('no_verbose'):
                    log.info('{} data source injected to mediator'.format(
                        name))
            else:
                # Do not create data source if configuration not found
                self.data_sources[name] = None
                log.warning('No {} data source injected: no configuration '
                            'found'.format(name))
        else:
            # Add variables to existing data source, if needed
            if variables is not None:
                self.data_sources[name].update_variables(variables)

        return self.data_sources[name]

    def add_multi_data_source(self, src_vars, parent=None):
        """Initialize multiple data source, inject to mediator,
        and return it as well.

        :param src_vars: Mapping with multiple (source name, variables list)
          (key, value) pairs, sequence of source names..
        :param parent: Container for which to add data source.
          Default is `None`.
        :type src_vars: mapping, or collection.
        :type parent: :py:class:`.container.Container`

        :returns: Multiple data-source.
        :rtype: :py:class:`.data_source.MultiDataSource`

        .. seealso:: :py:meth:`add_data_source`,
          :py:meth:`add_single_data_source`
        """
        if not isinstance(src_vars, collections.Mapping):
            # If a collection of source names is given, transform it
            # to a mapping from source names to None (variables)
            src_vars = {src_name: None for src_name in src_vars}

        data_sources = {}
        for src_name, variables in src_vars.items():
            # Add data source to mediator
            self.add_single_data_source(
                src_name, variables=variables, parent=parent)

            # Add data source to multi-data-source dictionary
            data_sources[src_name] = self.data_sources[src_name]

        # Verify that multi data source not already added by other containers
        multi_src_name = MultiDataSource.get_name(data_sources)
        if multi_src_name not in self.data_sources:
            # Create multiple data source from data sources dictionary
            multi_data_src = MultiDataSource(self, data_sources)

            # Inject multiple data-source to mediator
            self.data_sources[multi_src_name] = multi_data_src
        else:
            # Get existing multiple data-source
            multi_data_src = self.data_sources[multi_src_name]

            # Update multiple data-source with potential new data sources
            multi_data_src.update_data_sources(data_sources)

        return multi_data_src

    def _init_geo(self, **kwargs):
        """Initialize geographic data source and configuration."""
        self.geo_cfg = load_config(self.cfg, 'geo')
        src_name = self.geo_cfg['data']
        self.add_data_source(src_name)
        # Convenience member pointing to geo data source
        self.geo_src = self.data_sources[src_name]

    def _init_optimizer(self, **kwargs):
        """Initialize optimizer to associate to the given mediator."""
        # Add optimizer configuration
        opt_name = self.cfg.get('optimizer')
        if opt_name is not None:
            name = self.cfg['optimizer']
            cfg_opt = load_config(self.cfg, name)

            # Import data source module
            mod = import_module_from_cfg(cfg_opt, name=name)

            # Add data source to mediator
            self.optimizer = mod.Optimizer(self, cfg=cfg_opt, **kwargs)

            # Add optimizer as children
            self.update_children({self.optimizer.name: self.optimizer})

            if not self.cfg.get('no_verbose'):
                log.info('{} injected to mediator'.format(
                    self.optimizer.name))
        else:
            log.warn('No optimizer provided: skipping')

    def download_all(self, **kwargs):
        """Convenience method to download data of a given type
          for all components.

        .. seealso::
          :py:meth:`.data_source.DataSourceBase.manage_download`
        """
        for data_src in self.data_sources.values():
            data_src.manage_download(**kwargs)

    def get_data_all(self, **kwargs):
        """Convenience method to load data for all components.

        .. seealso:: :py:meth:`.data_source.DataSourceBase.get_data`
        """
        for data_src in self.data_sources.values():
            data_src.get_data(**kwargs)

    def get_mask_all(self, **kwargs):
        """Convenience method to make masks for all input data.

        .. seealso:: :py:meth:`.geo.GeoDataSourceBase.get_mask`
        """
        for data_src in self.gridded_sources:
            data_src.get_mask(**kwargs)

    def get_result_all(self, variables=None, **kwargs):
        """Convenience method to get output results for all components.

        :param variables: List of variables composing dataset.
          Default is `None`, in which case fit is performed for
          all variables in input data source.

        .. seealso:: :py:meth:`.component.Component.get_result`
        """
        for comp in self.components.values():
            comp.get_result(variables=variables, **kwargs)

    def __getitem__(self, comp_name):
        """Get component from :py:attr:`components`.

        :param comp_name: Component name.
        :type comp_name: str

        :returns: Component.
        :rtype: :py:class:`.component.Component`
        """
        return self.components[comp_name]

    def get(self, comp_name, default=None):
        """Get component from :py:attr`data`.

        :param comp_name: component name.
        :param default: Default value. Default is `None`.
        :type comp_name: str
        :type default: :py:class:`.component.Component`

        :returns: component.
        :rtype: :py:class:`.component.Component`
        """
        return self.components.get(comp_name, default)

    def __setitem__(self, comp_name, comp):
        """Set component in :py:attr:`data`.

        :param comp_name: component name.
        :param comp: Data of variable to set.
        :type comp_name: str
        :type comp: :py:class:`.component.Component`
        """
        self.components[comp_name] = comp

    def __contains__(self, comp_name):
        """Test if variable in data source.

        :param comp_name: component name.
        :type comp_name: str
        """
        return comp_name in self.components

    def __delitem__(self, comp_name):
        """Remove component from :py:attr:`components` set
        and from :py:attr:`data` mapping.

        :param comp_name: component name.
        :type comp_name: str
        """
        del self.components[comp_name]

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.components)

    def __len__(self):
        """Number of variables."""
        return len(self.components)


def _init_logger(cfg):
    """Initialize logger.

    :param cfg: Configuration including logger configuration.
    :type cfg: :py:class:`dict` or :py:class:`.config.Config`
    """
    log_path = cfg.get('log_path')
    log_level = cfg.get('log_level', 'INFO')
    log_fmt0 = ('%(asctime)s/%(name)s.%(funcName)s:%(lineno)d/'
                '%(levelname)s: %(message)s')
    log_fmt = cfg.get('log_fmt', log_fmt0)
    capture_warnings = cfg.get('capture_warnings', True)

    # Configure logger
    pkg_log = logging.getLogger(pkg_name)
    pkg_log.setLevel(log_level)

    # Create file or stream handler
    if log_path is not None:
        log_path = os.path.join(*ensure_collection(log_path))
        # If log_path given, log to file instead of stream
        msg = ('Setting loggging to {}. '
               'Open it for further information'.format(log_path))
        warn(msg)
        hdlr = logging.FileHandler(log_path, mode='a')
    else:
        hdlr = logging.StreamHandler()

    # Add formatter and set level
    formatter = logging.Formatter(log_fmt)
    hdlr.setFormatter(formatter)
    hdlr.setLevel(log_level)

    # Add handler to root and warnings
    pkg_log.addHandler(hdlr)
    if capture_warnings:
        logging.captureWarnings(capture_warnings)
        warn_log = logging.getLogger('py.warnings')
        warn_log.addHandler(hdlr)

    # Add matplotlib logger
    mpl_log = logging.getLogger('matplotlib')
    mpl_log.addHandler(hdlr)
