"""Actuator base definitions."""
import os
import logging
from abc import ABC, abstractmethod
import pickle
import xarray as xr
from sklearn.base import BaseEstimator, TransformerMixin
from .container import Container

#: Logger.
log = logging.getLogger(__name__)


class ActuatorBase(Container):
    """Actuator base class."""

    def __init__(self, output_variable, name, cfg=None, task_names=set(),
                 **kwargs):
        """Actuator constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param name: Estimator name.
        :param cfg: Estimator configuration. Default is `None`.
        :param task_names: Names of potential tasks for container to perform.
          Default is `set()`.
        :type output_variable: :py:class:`OutputVariable`
        :type name: str
        :type cfg: dict
        :type task_names: set
        """
        #: Data sources.
        self.data_sources = None

        # Attach component and output variable to actuator
        #: Output variable to act on.
        self.output_variable = output_variable
        #: Output-variable component.
        self.comp = self.output_variable.comp

        # Initialize as container
        kwargs.update({
            'comp': self.comp, 'name': name,
            'output_variable': output_variable,
            'cfg': cfg, 'med': self.comp.med, 'task_names': task_names})
        super(ActuatorBase, self).__init__(**kwargs)

        # Add data sources
        if 'data' in self.cfg:
            self.data_sources = {}
            self.add_data_sources(**kwargs)

            # Add data sources as children
            self.update_children(self.data_sources)

    def add_data_sources(self, **kwargs):
        """Add data sources from configuration."""
        for stage, src_vars in self.cfg['data'].items():
            # Add data source to mediator and output variable
            self.data_sources[stage] = self.med.add_data_source(
                src_vars, self.output_variable)


class EstimatorBase(ActuatorBase, BaseEstimator, ABC):
    """Estimator abstract base class. Requires :py:meth:`fit` and
    :py:meth:`predict` methods to be implemented."""

    def __init__(self, output_variable, name, cfg=None, **kwargs):
        """Estimator constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param name: Estimator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type name: str
        :type cfg: dict
        """
        #: Coefficients to be fitted
        self.coef = None

        # Try updating task names in keyword arguments if possible
        task_names = kwargs.get('task_names') or set()
        task_names.update({'fit', 'predict'})
        kwargs.update({
            'comp': output_variable.comp, 'name': name,
            'output_variable': output_variable,
            'cfg': cfg, 'med': output_variable.med, 'task_names': task_names})
        # Initialize as container
        super(EstimatorBase, self).__init__(**kwargs)

    @abstractmethod
    def fit(**kwargs):
        """Fit estimator abstract method."""
        raise NotImplementedError

    @abstractmethod
    def predict(**kwargs):
        """Predict with estimator abstract method."""
        raise NotImplementedError

    def get_estimator_postfix(self, **kwargs):
        """Default implementation: get an empty postfix string.

        :returns: Postfix.
        :rtype: str
        """
        return ''

    def get_fit_postfix(self, **kwargs):
        """Get fit postfix (component, feature, estimator).

        :returns: Postfix.
        :rtype: str
        """
        # Feature postfix
        feature_postfix = self.output_variable.feature[
            'fit'].get_data_postfix(**kwargs)

        # Output data postfix
        data_src = self.output_variable.output_extractor.data_sources[
            'output']
        output_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Estimator postfix
        estimator_postfix = self.get_estimator_postfix(**kwargs)

        # Fit postfix
        fit_postfix = '{}{}{}'.format(
            feature_postfix, output_postfix, estimator_postfix)

        return fit_postfix

    def get_fit_path(self, makedirs=True, **kwargs):
        """Get fit filepath.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Filepath.
        :rtype: str
        """
        filename = '{}_estimator{}'.format(
            self.comp.name, self.get_fit_postfix(**kwargs))
        data_dir = self.comp.get_data_dir(makedirs=makedirs, **kwargs)
        filepath = os.path.join(data_dir, filename)

        return filepath

    def read(self, **kwargs):
        """Read estimator with pickle."""
        try:
            # Try to read as netcdf data-array
            filepath = '{}.nc'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                log.info('Reading {} {} {} estimator from {}'.format(
                    self.comp.name, self.output_variable.name, self.name,
                    filepath))
            with xr.open_dataarray(filepath) as da:
                self.coef = da.copy(deep=True)
        except FileNotFoundError:
            # Read as pickle otherwise
            filepath = '{}.pickle'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                log.info('Reading {} {} {} estimator from {}'.format(
                    self.comp.name, self.output_variable.name, self.name,
                    filepath))
            with open(filepath, 'rb') as f:
                self.coef = pickle.load(f)

    def write(self, **kwargs):
        """Write estimator with pickle."""
        try:
            # Try to write as netcdf data-array
            filepath = '{}.nc'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                log.info('Writing {} {} {} estimator to {}'.format(
                    self.comp.name, self.output_variable.name, self.name,
                    filepath))
            self.coef.to_netcdf(filepath)
        except AttributeError:
            # Read as pickle otherwise
            filepath = '{}.pickle'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                log.info('Writing {} {} {} estimator to {}'.format(
                    self.comp.name, self.output_variable.name, self.name,
                    filepath))
            # Otherwise, write as pickle
            with open(filepath, 'wb') as f:
                pickle.dump(self.coef, f)


class FeatureExtractorBase(ActuatorBase, BaseEstimator, TransformerMixin, ABC):
    """Feature extractor base class.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self, output_variable, name, cfg=None, **kwargs):
        """Feature extractor constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param name: Estimator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type name: str
        :type cfg: dict
        """
        #: Estimation stages.
        self.stages = {'fit', 'predict'}

        #: Transformation flag. If `True`, no extraction is performed.
        self.no_extraction = False

        # Initialize as container
        task_names = set()
        for stage in self.stages:
            task_names.update({'extract_to_' + stage, 'write_' + stage})
        kwargs.update({
            'comp': output_variable.comp, 'name': name,
            'output_variable': output_variable,
            'cfg': cfg, 'med': output_variable.med, 'task_names': task_names})
        super(FeatureExtractorBase, self).__init__(**kwargs)

    @abstractmethod
    def transform(self, data_src, stage=None, **kwargs):
        """Abstract transform method."""
        raise NotImplementedError

    def get_feature_extractor_postfix(self, **kwargs):
        """Default implementation: get an empty feature postfix string.

        :returns: Postfix.
        :rtype: str
        """
        return ''


class DefaultFeatureExtractor(FeatureExtractorBase):
    """Default feature extractor implementation.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self, output_variable, cfg=None, **kwargs):
        """Default feature extractor constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param cfg: Estimator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type cfg: dict
        """
        name = 'default_feature_extractor'
        super(DefaultFeatureExtractor, self).__init__(
            output_variable=output_variable, name=name, cfg=cfg, **kwargs)

        # Flag that no transformation is to be performed
        self.no_extraction = True

    def transform(self, data_src, stage=None, **kwargs):
        """Default transform: return identical data source
        and prevent writing.

        :param data_src: Input data source.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
          May be required if features differ in prediction stage.
        :type data_src: :py:class:`..grid.DataSourceBase`
        :type stage: str
        """
        log.warning('No {} {} feature transformation performed'.format(
            self.comp.name, self.output_variable.name))

        # Prevent writing if same data
        self.task_mng['write_' + stage] = False

        # Return identical data
        return data_src


class OutputExtractorBase(ActuatorBase, BaseEstimator, TransformerMixin, ABC):
    """Output extractor abstract base class.
    Requires :py:meth:`transform` method to be implemented."""

    def __init__(self, output_variable, name, cfg=None, **kwargs):
        """Output extractor constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param name: Estimator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type name: str
        :type cfg: dict
        """
        #: Transformation flag. If `True`, no extraction is performed.
        self.no_extraction = False

        # Initialize as container
        task_names = {'extract_output', 'write_output'}
        kwargs.update({
            'comp': output_variable.comp, 'name': name,
            'output_variable': output_variable,
            'cfg': cfg, 'med': output_variable.med, 'task_names': task_names})
        super(OutputExtractorBase, self).__init__(**kwargs)

    @abstractmethod
    def transform(self, data_src, stage=None, **kwargs):
        """Abstract transform method."""
        raise NotImplementedError

    def get_output_extractor_postfix(self, **kwargs):
        """Default implementation: get an empty output postfix string.

        :returns: Postfix.
        :rtype: str
        """
        return ''


class DefaultOutputExtractor(OutputExtractorBase):
    """Default output extractor implementation.
    Requires :py:meth:`transform` method to be implemented."""

    def __init__(self, output_variable, cfg=None, **kwargs):
        """Default output extractor constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param cfg: Estimator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type cfg: dict
        """
        name = 'default_output_extractor'
        super(DefaultOutputExtractor, self).__init__(
            output_variable=output_variable, name=name, cfg=cfg, **kwargs)

        # Flag that no transformation is performed
        self.no_extraction = True

    def transform(self, data_src, **kwargs):
        """Default transform: return identical data source
        and prevent writing.

        :param data_src: Input data source.
        :type data_src: :py:class:`..grid.DataSourceBase`
        """
        log.warning('No {} {} output transformation performed'.format(
            self.comp.name, self.output_variable.name))

        # Prevent writing if same data
        self.task_mng['write_output'] = False

        # Return identical data
        return data_src


class ModifierBase(ActuatorBase, BaseEstimator, TransformerMixin, ABC):
    """Modifier abstract base class.
    Requires :py:meth:`apply` method to be implemented."""

    def __init__(self, output_variable, name, cfg=None, **kwargs):
        """Modifier constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param name: Estimator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type name: str
        :type cfg: dict
        """
        # Initialize as container
        task_names = {'initialize'}
        kwargs.update({
            'comp': output_variable.comp, 'name': name,
            'output_variable': output_variable,
            'cfg': cfg, 'med': output_variable.med, 'task_names': task_names})
        super(ModifierBase, self).__init__(**kwargs)

    def initialize(self, **kwargs):
        """Default initialization implementation: do nothing."""
        self.task_mng['initialize'] = False

    @abstractmethod
    def apply():
        """Modifier application abstract method."""
        raise NotImplementedError

    def get_modifier_postfix(self, **kwargs):
        """Default implementation: get an empty modifier postfix string.

        :returns: Postfix.
        :rtype: str
        """
        return ''
