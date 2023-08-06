"""Optimization base definitions."""
from abc import ABC, abstractmethod
import logging
from .config import load_config
from .container import Container
from .data_source import DataSourceBase, DataSourceLoaderBase

#: Logger.
log = logging.getLogger(__name__)


class OptimizerBase(Container, ABC):
    """Optimizer abstract base class. Requires :py:meth:`solve` method to be
    implemented."""

    def __init__(self, med, name, cfg=None, **kwargs):
        """Build optimizer linked to mediator.

        :param med: Mediator.
        :param name: Optimizer name.
        :param cfg: Optimizer configuration.
          If `None`, call :py:meth:`.config._load_src_coonfig`.
          Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        # Load optimizer configuration
        loaded_cfg = cfg or load_config(self.med.cfg, self.name)

        # Initialize as container
        task_names = ['solve']
        super(OptimizerBase, self).__init__(
            med, name, cfg=loaded_cfg, task_names=task_names, **kwargs)

        #: Input data-source.
        self.input = None

        #: Solution data-source.
        self.solution = SolutionBase(self, **kwargs)

    @abstractmethod
    def solve(self, *args, **kwargs):
        """Abstract method to solve optimization problem."""
        raise NotImplementedError

    def get_solution(self, **kwargs):
        """Get optimization solution by solving optimization problem,
        if needed, after loading input data, if needed."""
        if self.task_mng.get('solve'):
            # Get input data
            self.input.get_data(**kwargs)

            # Solve optimizatioon
            self.solve(**kwargs)

            # Update task manager
            self.task_mng['solve'] = False

            # Write single solution
            self.solution.write(**kwargs)
        else:
            # Read solution
            if not self.cfg.get('no_verbose'):
                log.info('{} optimization problem already solved'.format(
                    self.name))
            self.solution.read(**kwargs)


class InputBase(DataSourceLoaderBase):
    """Abstract optimization input class as data source with loader.
    Requires :py:meth:`load` method inherited from
    :py:class:`.data_source.DataSourceLoaderBase` to be implemented."""

    def __init__(self, opt, cfg=None, **kwargs):
        """Initialize input data-source.

        :param opt: Optimizer.
        :param cfg: Input configuration. Default is `None`.
        :type opt: :py:class:`.optimization.OptimizerBase`
        :type cfg: dict
        """
        self.opt = opt
        name = '{}_input'.format(self.opt.name)

        super(InputBase, self).__init__(self.opt.med, name, cfg=cfg, **kwargs)

    def get_data_postfix(self, **kwargs):
        """Get data postfix.

        :returns: Postfix.
        :rtype: str
        """
        return ''

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self.opt, subdirs='input', makedirs=makedirs)


class SolutionBase(DataSourceBase):
    """Optimization solution base class as data source."""

    def __init__(self, opt, cfg=None, **kwargs):
        """Initialize solution as data source.

        :param opt: Optimizer.
        :param cfg: Solution configuration. Default is `None`.
        :type opt: :py:class:`.optimization.OptimizerBase`
        :type cfg: dict
        """
        self.opt = opt
        name = '{}_solution'.format(self.opt.name)

        super(SolutionBase, self).__init__(
            self.opt.med, name, cfg=cfg, task_names=None, **kwargs)

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self.opt, subdirs='solution', makedirs=makedirs)

    def get_data_postfix(self, **kwargs):
        """Default implementation of get optimization results postfix.

        :returns: Postfix.
        :rtype: str
        """
        return self.opt.input.get_data_postfix()
