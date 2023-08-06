"""Data-source base definitions."""
from abc import ABC, abstractmethod
import os
from collections import MutableMapping
import logging
import functools
import xarray as xr
from netCDF4 import Dataset as nc_Dataset
from .container import Container, ensure_collection

#: Logger.
log = logging.getLogger(__name__)


class DataSourceBase(Container, MutableMapping):
    """Base data source class for APIs."""

    def __init__(self, med, name, cfg=None, variables=None, task_names=None,
                 **kwargs):
        """Build data source linked to mediator.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :param variables: Name(s) of variable(s) composing dataset.
          Default is `None`.
        :param task_names: Names of potential tasks for container to perform.
          Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        :type variables: (collection of) :py:class:`str`
        :type task_names: set
        """
        # Add read tasks
        if variables is not None:
            variables = ensure_collection(variables, set)
            if task_names is None:
                task_names = set()
            for variable in variables:
                task_names.add('read_{}'.format(variable))

        # Initialize as container
        super(DataSourceBase, self).__init__(
            med, name, cfg=cfg, task_names=task_names, **kwargs)

        #: Whether this is a gridded data-source.
        #: By default, data source not gridded.
        self.gridded = False

        #: Data-source data. 
        self.data = {}

        #: Data-source variables.
        self.variables = set()

        # Add (ensured) list of variables composing dataset
        if variables is not None:
            self.update_variables(variables)

    def update_variables(self, variables, **kwargs):
        """Add variables to data source.

        :param variables: (List of) name(s) of variable(s) to add.
        :type variable: (collection of) :py:class:`str`
        """
        variables = ensure_collection(variables, set)

        # Update variables set
        self.variables.update(variables)

        # Update tasks
        for variable in variables:
            task_name = 'read_{}'.format(variable)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})

    def __getitem__(self, variable):
        """Get variable data from :py:attr:`data`.

        :param variable: Variable name.
        :type variable: str

        :returns: Variable.
        :rtype: :py:class:`xarray.DataArray`

        .. note: Calls `__getitem__` method from :py:class:`dict`.
        """
        return self.data[variable]

    def get(self, variable, default=None):
        """Get variable data from :py:attr`data`.

        :param variable: Variable name.
        :param default: Default value. Default is `None`.
        :type variable: str
        :type default: :py:class:`xarray.DataArray`

        :returns: Variable.
        :rtype: :py:class:`xarray.DataArray`

        .. note: Calls `get` method from :py:class:`dict`.
        """
        return self.data.get(variable, default)

    def __setitem__(self, variable, data):
        """Set item in :py:attr:`data`.

        :param variable: Variable name.
        :param data: Data of variable to set.
        :type variable: str
        :type data: :py:class:`xarray.DataArray`

        .. note: Calls `__setitem__` method from :py:class:`dict`.
        """
        self.data[variable] = data

    def __contains__(self, variable):
        """Test if variable in data source.

        :param variable: Variable name.
        :type variable: str
        """
        return variable in self.variables

    def __delitem__(self, variable):
        """Remove variable from :py:attr:`variables` set
        and from :py:attr:`data` mapping.

        :param variable: Variable name.
        :type variable: str
        """
        # Remove variable
        self.variables.remove(variable)
        # Remove data for variable
        del self.data[variable]

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.data)

    def __len__(self):
        """Number of variables."""
        return len(self.variables)

    def __str__(self):
        """Get dataset as string."""
        s = "<{} '{}'>\n".format(str(self.__class__)[8:-2], self.name)
        s += '{}'.format(self.data)

        return s

    def update(self, var_data):
        """Update data with given dataset.

        :param var_data: Dataset.
        :type var_data: Mapping of :py:class:`xarray.DataArray`
        """
        # Update variable list
        self.variables.update(var_data.keys())

        # Update data
        self.data.update(var_data)

    def copy_data(self, data_src, variable=None):
        """Copy data from another data source, e.g.
        of type :py:class:`Prediction` or :py:class:`Feature`.

        :param data_src: Data source to copy.
        :param variable: Name of a specific variable from which
          to copy data. Default is `None`
        :param data_src: :py:class:`.data_sources.`DataSourceBase`
        :param variable: str
        """
        if variable is not None:
            self.update({variable: data_src.get(variable)})
        else:
            self.update(data_src.data)

    def close(self, variables=None):
        """Close dataset.

        :param variables: Variable(s) to close. Default is `None`,
          in which case all variables are closed.
        :type variables: (collection of) :py:class:`str`
        """
        # Get variables list
        variables = ensure_collection(variables or self.variables)

        # Close each variable separately
        for variable in variables:
            self.data[variable].close()

    def read(self, variables=None, **kwargs):
        """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

        :param variables: Variable(s) to read. Default is `None`,
          in which case variables are read.
        :type variables: (collection of) :py:class:`str`
        """
        variables = ensure_collection(variables or self.variables)
        # Get data filepath
        filepath = '{}.nc'.format(self.get_data_path(
            makedirs=False, **kwargs))

        # Try getting variables list from arguments, attribute, groups
        if not variables:
            with nc_Dataset(filepath, 'r') as nc_ds:
                variables = nc_ds.groups.keys()

        if variables:
            # Update data source set of variables
            self.update_variables(variables)

            # Read each variable separately
            ds = {}
            for iv, variable in enumerate(variables):
                if self.task_mng['read_{}'.format(variable)]:
                    if not self.cfg.get('no_verbose'):
                        log.info('Reading {} {} from {}'.format(
                            self.name, variable, filepath))
                    try:
                        # Try to read as dataarray
                        with xr.open_dataarray(
                                filepath, group=variable) as da:
                            ds[variable] = da.copy(deep=True)
                    except ValueError:
                        # Or else read as dataset
                        with xr.open_dataset(filepath, group=variable) as da:
                            ds[variable] = da.copy(deep=True)

                    # Update task manager
                    self.task_mng['read_{}'.format(variable)] = False
                else:
                    # Skip
                    if not self.cfg.get('no_verbose'):
                        log.info('{} {} already read: skipping'.format(
                            self.name, variable))

            # Update dataset
            self.update(ds)
        else:
            log.warning('Empty variable list given: no {} data '
                        'read'.format(self.name))

    def write(self, variables=None, **kwargs):
        """Write :py:class:`xarray.DataArray` of each variable in netcdf.

        :param variables: Variable(s) to write. Default is `None`,
          in which all variables are written.
        :type variables: (collection of) :py:class:`str`
        """
        variables = ensure_collection(variables or self.variables)

        if variables:
            filepath = '{}.nc'.format(self.get_data_path(**kwargs))
            # Write each variable separately
            for iv, variable in enumerate(variables):
                if not self.cfg.get('no_verbose'):
                    log.info('Reading {} {} from {}'.format(
                        self.name, variable, filepath))
                # Overwrite file for first variable,
                # overwrite variables otherwise
                mode = 'a' if iv else 'w'
                self.get(variable).to_netcdf(
                    filepath, group=variable, mode=mode)
        else:
            log.warning('Empty variable list given: no {} data '
                        'written'.format(self.name))

    def get_postfix(self, **kwargs):
        """Return empty postfix string.

        returns: Postfix.
        rtype: str
        """
        return ''

    def get_data_postfix(self, with_src_name=False, **kwargs):
        """Get data-source postfix.
        A user-defined postfix may be defined in the `'postfix'`
        entry of the data-source configuration.
        Otherwise, the standard postfix is used by calling
        :py:meth:`get_postfix`.
        The data-source name is prepended.

        :param with_src_name: Whether to prefix postfix with source name.
        :type with_src_name: bool

        :returns: Postfix.
        :rtype: str
        """
        # Get user-defined postfix or standard postfix
        postfix = self.cfg.get('postfix')
        postfix = (self.get_postfix(**kwargs) if postfix is None else
                   postfix)

        # Prepend data-source name
        if with_src_name:
            postfix = '_{}{}'.format(self.name, postfix)

        return postfix

    def get_data_path(self, variable=None, makedirs=True, **kwargs):
        """Get data-source filepath.

        :param variable: Data variable. Default is `None`.
        :param makedirs: Make directories if needed. Default is `True`.
        :type variable: str
        :type makedirs: bool

        :returns: Filepath.
        :rtype: str
        """
        var_pf = '_{}'.format(variable) if variable else ''
        data_pf = self.get_data_postfix(variable=variable, **kwargs)
        filename = '{}{}_{}{}'.format(
            self.name, var_pf, self.med.cfg['area'], data_pf)
        data_dir = self.get_data_dir(makedirs=makedirs, **kwargs)
        filepath = os.path.join(data_dir, filename)

        return filepath


class MultiDataSource(DataSourceBase, MutableMapping):
    def __init__(self, med, data_sources, task_names=set(),
                 default_tasks_value=True, **kwargs):
        """Build data source composed to multiple data-sources
        and linked to mediator.

        :param med: Mediator.
        :param data_sources: Data sources dictionary.
        :param task_names: Names of potential tasks for container to perform.
          Default is `set()`.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none. Default is `True`.
        :type med: :py:class:`.mediator.Mediator`
        :type data_sources: :py:class:`dict` of :py:class:`DataSourceBase`
        :type task_names: set
        :type default_tasks_value: bool

        .. warn:: At the moment, a variable can only belong to one data source.
        """
        # Multiple-data-source attributes specification
        cfg = None
        name = self.get_name(data_sources)

        # Initialize as data source
        super(MultiDataSource, self).__init__(
            med, name, cfg=cfg, task_names=task_names,
            default_tasks_value=default_tasks_value, **kwargs)

        #: Data sources composing multiple data-source.
        self.data_sources = {}

        #: Variable to data source mapping and variables list
        #: (for it to be useful, we need to assume that one and only one
        #: dataset is associated to a variable.
        #: This may be improved by adding information
        #: on the data source to variables names).
        self.var_data_src = {}

        # Update with data sources
        self.update_data_sources(data_sources)

    @staticmethod
    def get_name(data_sources):
        """Get class name from data_sources.

        :param data_sources: Data sources list.
        :type data_sources: :py:class:`list` of :py:class:`DataSourceBase`

        :returns: Multiple-data-source name.
        :rtype: str
        """
        # Note: in principle, data_sources' keys correspond to name
        # attribute of each data_src
        return '__'.join(data_src.name for data_src in data_sources.values())

    def update_data_sources(self, data_sources):
        """Update :py:attr:`data_sources` and :py:attr:`variables`.

        :param data_sources: Data sources dictionary.
        :type data_sources: :py:class:`dict` of :py:class:`DataSourceBase`
        """
        for src_name, data_src in data_sources.items():
            # Update data sources
            self.data_sources.update({src_name: data_src})

            # Update variables
            self.update_variables(data_src.variables)

            # Update variable to data source mapping
            self.var_data_src.update(
                {var: data_src for var in data_src.variables})

            # Check if gridded
            if data_src.gridded:
                self.gridded = True

            # Add data sources as children
            self.update_children(self.data_sources)

    def __getitem__(self, variable):
        """Get item from data source containing variable.

        :param variable: Variable name.
        :type variable: str

        :returns: Variable.
        :rtype: :py:class:`xarray.DataArray`
        """
        # Data source containing variable
        data_src = self.get_data_source(variable)

        return data_src[variable]

    def __str__(self):
        """Get dataset as string."""
        s = "<{} '{}'>\n".format(str(self.__class__)[8:-2], self.name)
        s += '\n'.join('{}\n{}'.format(str(data_src), str(data_src.data))
                       for data_src in self.data_sources.values())

        return s

    def get(self, variable, default=None):
        """Get variable from data source containing variable.

        :param variable: Variable name.
        :param default: Default value. Default is `None`.
        :type variable: str
        :type default: str

        :returns: Variable.
        :rtype: :py:class:`xarray.DataArray`
        """
        # Data source containing variable
        data_src = self.get_data_source(variable)

        return (data_src.get(variable, default) if data_src is not None
                else None)

    def get_data_source(self, variable):
        """Get single data source containing variable.

        :param variable: Variable name.
        :type variable: str

        :returns: Data source.
        :rtype: :py:class:`DataSourceBase`
        """
        return self.var_data_src.get(variable)

    def __setitem__(self, variable, data):
        """Set item in data source containing variable.

        :param variable: Variable name.
        :param data: Data of variable to set.
        :type variable: str
        :type data: :py:class:`xarray.DataArray`
        """
        # Data source containing variable
        data_src = self.var_data_src[variable]

        # Set variable in data source
        data_src[variable] = data

    def update(self, var_data):
        """Update data with given dataset.

        :param var_data: Dataset.
        :type var_data: Mapping of :py:class:`xarray.DataArray`
        """
        for variable, data in var_data.items():
            # Single data-source containing variable
            data_src = self.var_data_src[variable]

            # Update single data-source
            data_src.data.update({variable: data})

        # Update multi-data-source variables
        self.update_variables(var_data.keys())

    def download(self, variables=None, **kwargs):
        """Download multiple data-source calling :py:meth:`DataSourceBase.download`
        of each data source.

        .. seealso:: :py:meth:`DataSourceBase.download`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                data_src.download(variables=variables, **kwargs)

    def manage_download(self, **kwargs):
        """Manage multiple data-source download calling
        :py:meth:`DataSourceBase.manage_download` of each data source.

        .. seealso:: :py:meth:`DataSourceBase.manage_download`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                data_src.manage_download(**kwargs)

    def load(self, variables=None, **kwargs):
        """Retrieve multiple data-source.

        :returns: Multiple datasets.
        :rtype: Mapping of mapping of :py:class:`xarray.DataArray`

        .. seealso:: :py:meth:`DataSourceBase.load`
        """
        d = {}
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                d[data_src.name] = data_src.load(
                    variables=variables, **kwargs)

        return d

    def get_data(self, **kwargs):
        """Load data from multiple data-sources calling
        :py:meth:`DataSourceBase.get_data` of each data source.

        .. seealso:: :py:meth:`DataSourceBase.get_data`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                # Get data for single source, transmitting keywords
                data_src.get_data(**kwargs)

    def get_mask(self, **kwargs):
        """Get mask for gridded single-data-sources calling
        :py:meth:`GriddedDataSourceBase.get_mask`.

        .. seealso:: :py:meth:`GriddedDataSourceBase.get_mask`
        """
        for data_src in self.data_sources.values():
            if data_src.gridded:
                # Get data for single source, transmitting keywords
                data_src.get_mask(**kwargs)

    def read(self, variables=None, **kwargs):
        """Read multiple data-source.

        .. seealso:: :py:meth:`DataSourceBase.read`
        """
        for src_label, data_src in self.data_sources.items():
            data_src.read(variables=variables, **kwargs)

    def write(self, variables=None, **kwargs):
        """Write multiple data-source.

        .. seealso:: :py:meth:`DataSourceBase.write`
        """
        for data_src in self.data_sources.values():
            data_src.write(variables=variables, **kwargs)

    def get_data_postfix(self, variable=None, with_src_name=False, **kwargs):
        """Get multiple data-source postfix as sum of each single
        data source postfix.

        :param variable: Data variable. Default is `None`.
        :param with_src_name: Whether to prefix postfix with source name.
        :type variable: str
        :type with_src_name: bool

        :returns: Postfix.
        :rtype: str
        """
        if (variable is not None) and (variable in self.var_data_src):
            postfix = self.get_data_source(variable).get_data_postfix(
                variable=variable, with_src_name=with_src_name, **kwargs)
        else:
            postfix = ''.join(data_src.get_data_postfix(
                with_src_name=with_src_name, **kwargs)
                for data_src in self.data_sources.values())

        return postfix


class DataSourceLoaderBase(DataSourceBase, ABC):
    """Data-source loader base class. Requires :py:meth:`load` method
    to be implemented. Also includes a passing :py:meth:`download` method."""

    def __init__(self, med, name, cfg=None, variables=None, **kwargs):
        """Build data source with downloading and loading capabilities.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :param variables: List of variables composing dataset.
          Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        :type variables: (collection of) :py:class:`str`
        """
        task_names = {'download', 'load'}
        super(DataSourceLoaderBase, self).__init__(
            med, name, cfg=cfg, variables=variables, task_names=task_names,
            **kwargs)

    @abstractmethod
    def load(self, variables=None, **kwargs):
        """Retrieve data from the input source and return an object."""
        raise NotImplementedError

    def download(self, variables=None, **kwargs):
        """Download data."""
        log.warning('{} download not implemented'.format(self.name))

    def get_data(self, **kwargs):
        """Read or load data from a given source and store it in
        :py:attr:`data` member.

        .. todo:: Handle variable selection.
        """
        # Read or load data
        if self.task_mng.get('load'):
            # Download data if needed
            self.manage_download(**kwargs)

            # Load data
            if not self.cfg.get('no_verbose'):
                log.info('Loading {} data'.format(self.name))
            self.update(self.load(**kwargs))

            # Write data (all components, in case more than one)
            self.write(**kwargs)

            # Update task manager
            self.task_mng['load'] = False
        else:
            # Read data
            if not self.cfg.get('no_verbose'):
                log.info('{} data already loaded'.format(self.name))
            self.read(**kwargs)

    def manage_download(self, **kwargs):
        """Manage data download."""
        if self.task_mng.get('download'):
            if not self.cfg.get('no_verbose'):
                log.info('Downloading {} data'.format(
                    ', '.join(self.name.split('__'))))
            self.download(**kwargs)

            # Update task manager
            self.task_mng['download'] = False


class Composer(object):
    """Compose functions.
    `Compose(f, g, h, **kwargs)(ds) = h(g(f(ds, **kwargs), **kwargs), **kwargs)`.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        #: Functions to compose.
        self._functions = args

        #: Composed function.
        self.composed = functools.reduce(
            lambda f, g: lambda ds, **kwargs_add: g(
                ds=f(ds=ds, **kwargs, **kwargs_add), **kwargs, **kwargs_add),
            self._functions, lambda ds, **kwargs_add: ds)

    def __call__(self, ds, **kwargs_add):
        """Caller."""
        return self.composed(ds=ds, **kwargs_add)
