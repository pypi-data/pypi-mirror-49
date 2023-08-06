"""Component and output-variable base definitions."""
import logging
from importlib import import_module
from collections import MutableMapping
from .config import load_config
from .container import Container, ensure_collection
from .data_source import DataSourceBase, MultiDataSource
from . import actuator_base

#: Logger.
log = logging.getLogger(__name__)


class OutputVariable(Container):
    """Output variable associated with a component."""

    def __init__(self, comp, name, cfg=None, **kwargs):
        """Output variable constructor.

        :param comp: Component to which variable is associated.
        :param name: Output variable name.
        :param cfg: Output variable configuration. Default is `None`.
        :type comp: :py:class:`Component`
        :type name: str
        :type cfg: dict
        """
        #: Output-variable component
        self.comp = comp

        #: Actuators.
        self.actuators = {}

        #: Data sources.
        self.data_sources = {}

        #: Features for each stage. Used in feature-extraction cases.
        self.feature = None
            
        #: Output data-source.
        self.output = None
        #: Prediction result data-source.
        self.prediction = None
        #: Result data-source.
        #: Identical to either :py:attr:`output` or :py:attr:`prediction`.
        self.result = None

        # Initialize as container
        super(OutputVariable, self).__init__(
            med=self.comp.med, name=name, cfg=cfg, **kwargs)

        # Initialize actuators from configuration
        for actuator_name in self.cfg:
            self.add_actuator(actuator_name=actuator_name, **kwargs)

        # Add actuators add children containers
        self.update_children(self.actuators)

        # Add data sources required by output variable (from all of its
        # actuators)
        for actuator in self.actuators.values():
            if actuator.data_sources is not None:
                for data_src in actuator.data_sources.values():
                    # Add as single data-source
                    self.data_sources.update({data_src.name: data_src})

                    # Add as single data-sources from multiple data-source
                    if isinstance(data_src, MultiDataSource):
                        self.data_sources.update({
                            single_data_src.name: single_data_src
                            for single_data_src in
                            data_src.data_sources.values()})

        # Initialize data attributes
        self._init_data_attributes(**kwargs)

    def add_actuator(self, actuator_name=None, actuator=None,
                     actuator_class_name='Actuator', **kwargs):
        """Add actuator (extractor, estimator, modifier, etc.).

        :param actuator_name: Actuator name. Default is `None`.
        :param actuator: Actuator. Default is `None`, in which case
          it is built with :py:meth:`_init_actuator`.
        :param actuator_class_name: Actuator class to call from module.
          Default is `'Actuator'`.
        :type actuator_name: str
        :type actuator: :py:class:`.container.Container`
        :type actuator_class_name: str
        """
        if actuator is None:
            if actuator_name in self.cfg:
                actuator_cfg = self.cfg[actuator_name]
                actuator_module = import_module_from_cfg(
                    actuator_cfg, name=actuator_name)

                if actuator_module is None:
                    # Get default extractor
                    actuator_class_name = 'Default' + ''.join(
                        act_name.title()
                        for act_name in actuator_name.split('_'))
                    actuator_module = actuator_base
                    log.warning(
                        '    No "module_path" found in {} configuration: '
                        'using {} class actuator'.format(
                            actuator_name, actuator_class_name))

                # Try to get actuator
                if hasattr(actuator_module, actuator_class_name):
                    actuator = getattr(actuator_module, actuator_class_name)(
                        self, cfg=actuator_cfg)
                else:
                    raise AttributeError(
                        'No {} class found in {} module for {} {} '
                        'actuator'.format(
                            actuator_class_name, actuator_module,
                            self.name, actuator_name))

        if actuator is not None:
            if not self.cfg.get('no_verbose'):
                log.info('Injecting {} actuator in {} {}'.format(
                    actuator_name, self.comp.name, self.name))
            # Add given actuator as attribute
            setattr(self, actuator_name, actuator)

            # Reference actuator in actuators set
            self.actuators[actuator_name] = actuator

    def _init_data_attributes(self, **kwargs):
        """Initialize data attributes."""
        # Initialize sources associated with results
        self.output = Output(self, **kwargs)
        self.prediction = Prediction(self, **kwargs)

        # Assign result
        if hasattr(self, 'estimator'):
            # to prediction
            self.result = self.prediction
        else:
            # to output
            self.result = self.output

        # Initialize features, associated with inputs
        if hasattr(self, 'feature_extractor'):
            self.feature = {}
            for stage in self.feature_extractor.stages:
                self.feature[stage] = Feature(self, stage=stage, **kwargs)

    def extract_feature(self, stage, **kwargs):
        """Extract or read the feature of a given component from input data,
        store it in the :py:attr:`feature` member, and save it to file.

        :param stage: Modeling stage: `'fit'` or `'predict'`.
        :type stage: str
        """
        if self.feature_extractor.task_mng.get('extract_to_' + stage):
            # Extract feature
            # Get input data source
            data_src = self.feature_extractor.data_sources[stage]
            if not self.cfg.get('no_verbose'):
                log.info('Extracting {} feature to {} {} from {}'.format(
                    self.comp.name, stage, self.name, data_src.name))

            if data_src.gridded:
                # Make mask for gridded data source
                data_src.get_mask(**kwargs)

            # Extract feature from the input data
            self.feature[stage].update(
                self.feature_extractor.transform(
                    data_src, stage=stage, **kwargs))

            # Write feature
            if self.feature_extractor.task_mng.get('write_' + stage):
                self.feature[stage].write(**kwargs)

            # Update task manager
            self.feature_extractor.task_mng['extract_to_' + stage] = False
        else:
            # Read feature
            if not self.cfg.get('no_verbose'):
                log.info(
                    '{} feature to {} {} already extracted'.format(
                        self.comp.name, stage, self.name))
            self.feature[stage].read(**kwargs)

    def fit(self, **kwargs):
        """Fit estimator for a given component.

        .. note:: Input and output data for the fitting are read from file.
          They should thus be extracted before.
        """
        # Read or fit
        stage = 'fit'
        if hasattr(self, 'estimator'):
            if self.estimator.task_mng.get(stage):
                # Get input feature
                self.extract_feature(stage, **kwargs)

                # Get output data
                self.extract_output(**kwargs)

                # Fit estimator
                if not self.cfg.get('no_verbose'):
                    log.info('Fitting {} {} estimator'.format(
                        self.comp.name, self.name))
                self.estimator.fit(self.feature[stage], self.output, **kwargs)

                # Save the fitted estimator
                self.estimator.write(**kwargs)

                # Update task managern
                self.estimator.task_mng[stage] = False
            else:
                # Load the estimator coefficients from file
                if not self.cfg.get('no_verbose'):
                    log.info('{} {} estimator already fitted'.format(
                        self.comp.name, self.name))
                self.estimator.read(**kwargs)
        else:
            if not self.cfg.get('no_verbose'):
                log.info('No estimator provided: skipping.')

    def predict(self, **kwargs):
        """Predict for a given component and store result to
        :py:attr:`prediction` member.

        .. note:: Input data for the prediction is read from file.
          It should thus be extracted before.
        """
        stage = 'predict'
        if hasattr(self, 'estimator'):
            if self.estimator.task_mng.get(stage):
                # Get estimator
                self.fit(**kwargs)

                # Get feature to predict
                self.extract_feature(stage, **kwargs)

                # Apply
                if not self.cfg.get('no_verbose'):
                    log.info('Predicting {} {}'.format(
                        self.comp.name, self.name))
                self.prediction.update(self.estimator.predict(
                    self.feature[stage], **kwargs))

                # Save
                # Warning: input data to fit estimator will be forgotten
                self.prediction.write(**kwargs)

                # Update task manager
                self.estimator.task_mng[stage] = False
            else:
                # Read prediction
                if not self.cfg.get('no_verbose'):
                    log.info('{} {} already predicted'.format(
                        self.comp.name, self.name))
                self.prediction.read(variables=self.name, **kwargs)
        else:
            if not self.cfg.get('no_verbose'):
                log.info('No {} {} estimator provided: skipping.'.format(
                    self.comp.name, self.name))

    def extract_output(self, **kwargs):
        """Extract or read ouptut of a given component from input data, store
        it in the :py:attr:`output` member, and save it to file.

        .. note:: The responsability to load the source data is left
          to the output extractor.
        """
        if self.output_extractor.task_mng.get('extract_output'):
            # Extract output
            # Get output data source in case needed
            stage = 'output'
            data_src = self.output_extractor.data_sources[stage]
            if not self.cfg.get('no_verbose'):
                log.info('Extracting {} {} output data from {}'.format(
                    self.comp.name, self.name, data_src.name))

            # Get data
            data_src.get_data(**kwargs)

            if data_src.gridded:
                # Make mask for gridded data sources (probably never used)
                self.data_src.get_mask(**kwargs)

            # Extract feature from the input data
            self.output.update(self.output_extractor.transform(
                data_src, **kwargs))

            # Write output
            if self.output_extractor.task_mng.get('write_output'):
                self.output.write(**kwargs)

            # Update task manager
            self.output_extractor.task_mng['extract_output'] = False
        else:
            # Read output data
            if not self.cfg.get('no_verbose'):
                log.info('{} {} output data already extracted:'.format(
                    self.comp.name, self.name))
            self.output.read(variables=self.name, **kwargs)

    def get_result(self, **kwargs):
        """Get output from prediction if :py:attr:`estimator` is not `None`,
        or directly from (extracted) output data source, and store it in
        :py:attr:`result`.
        """
        if hasattr(self, 'estimator'):
            # Predict
            self.predict(**kwargs)
        else:
            if not self.cfg.get('no_verbose'):
                log.info(
                    'No {} {} estimator provided: directly extracting '
                    'output data'.format(self.comp.name, self.name))
            # Get data
            self.extract_output(**kwargs)


class Component(Container, MutableMapping):
    """Component."""

    def __init__(self, med, name, cfg=None, out_var_names=None, **kwargs):
        """Initialize component attached to mediator.

        :param med: Mediator.
        :param name: Component name.
        :param cfg: Component configuration. Default is `None`, in which case
          it is loaded by :py:func:`.config.load_config`.
          Otherwise, none. Default is `True`.
        :param out_var_names: (List of) name(s) of variable(s)
          to estimate for component.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        :type out_var_names: (collection of) :py:class:`str`
        """
        # Load component configuration
        loaded_cfg = (cfg or load_config(med.cfg, name))

        #: Component output-variables.
        self.output_variables = {}

        #: Component data-sources.
        #: Union of data-sources from all the component output-variables.
        self.data_sources = {}

        #: Result.
        self.result = {}

        # Initialize as container
        super(Component, self).__init__(med, name, cfg=loaded_cfg, **kwargs)

        # Add output variables
        out_var_names = ensure_collection(out_var_names)
        for var_name in out_var_names:
            if not self.cfg.get('no_verbose'):
                log.info('Injecting {} variable in {} component'.format(
                    var_name, self.name))
            self.output_variables[var_name] = OutputVariable(
                self, var_name, cfg=self.cfg[var_name])

        # Add output variables as children
        self.update_children(self.output_variables)

        # Add data sources required by component (from all of its
        # output variables)
        for out_var in self.output_variables.values():
            self.data_sources.update(out_var.data_sources)

    def get_result(self, out_var_names=None, **kwargs):
        """Get results from all (given) output variables and store them in
        :py:attr:`result` (i.e. `self.result[out_var_name] =
        self.output_variables[out_var_name].data[out_var_name]`).

        :param out_var_names: (List of) name(s) of output variable(s)
          to estimate for component.
        :type out_var_names: (collection of) :py:class:`str`
        """
        out_var_names = (ensure_collection(out_var_names)
                         if out_var_names else self.output_variables.keys())

        for out_var_name in out_var_names:
            out_var = self[out_var_name]

            # Get result for this output variable
            out_var.get_result()

            # Store result data for this variable (convenience)
            self.result.update(out_var.result.data)

    def __getitem__(self, out_var_name):
        """Get output variable from :py:attr:`output_variables`.

        :param out_var_name: Output variable name.
        :type out_var_name: str

        :returns: Output variable.
        :rtype: :py:class:`OutputVariable`
        """
        return self.output_variables[out_var_name]

    def get(self, out_var_name, default=None):
        """Get output variable from :py:attr`data`.

        :param out_var_name: Output variable name.
        :param default: Default value. Default is `None`.
        :type out_var_name: str
        :type default: :py:class:`OutputVariable`

        :returns: Output variable.
        :rtype: :py:class:`OutputVariable`
        """
        return self.output_variables.get(out_var_name, default)

    def __setitem__(self, out_var_name, output_variable):
        """Set output_variable in :py:attr:`data`.

        :param out_var_name: Output variable name.
        :param output_variable: Data of variable to set.
        :type out_var_name: str
        :type output_variable: :py:class:`OutputVariable`
        """
        self.output_variables[out_var_name] = output_variable

    def __contains__(self, out_var_name):
        """Test if variable in data source.

        :param out_var_name: Output variable name.
        :type out_var_name: str
        """
        return out_var_name in self.output_variables

    def __delitem__(self, out_var_name):
        """Remove output variable from :py:attr:`output_variables` set
        and from :py:attr:`data` mapping.

        :param out_var_name: Output variable name.
        :type out_var_name: str
        """
        del self.output_variables[out_var_name]

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.output_variables)

    def __len__(self):
        """Number of variables."""
        return len(self.output_variables)


class OutputVariableDataSourceBase(DataSourceBase):
    """Base component data."""

    def __init__(self, output_variable, name=None, **kwargs):
        """Initialize feature as data source.

        :param output_variable: Output variable to which data is associated.
        :param name: Data name.
        :type output_variable: :py:class:`.component.OutputVariable`
        :type name: str
        """
        # Attach component and output variable
        #: Data-source output-variable .
        self.output_variable = output_variable
        #: Output-variable component.
        self.comp = self.output_variable.comp

        kwargs.update({
            'med': self.comp.med, 'name': name,
            'cfg': self.output_variable.cfg, 'task_names': None})
        super(OutputVariableDataSourceBase, self).__init__(**kwargs)

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self.comp, makedirs=makedirs)


class Feature(OutputVariableDataSourceBase):
    """Feature data source."""

    def __init__(self, output_variable, stage, **kwargs):
        """Initialize feature as data source.

        :param output_variable: Output variable to which data is associated.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
        :type output_variable: str
        :type stage: str
        """
        #: Data-source estimation-stage.
        self.stage = stage

        # Build component data source
        name = '{}_{}_feature_{}'.format(
            output_variable.comp.name, output_variable.name, self.stage)
        super(Feature, self).__init__(
            output_variable=output_variable, name=name,
            task_names=None, **kwargs)

        # Plug get_data_path method from feature_extractor if possible
        if hasattr(self.output_variable.feature_extractor, 'get_data_path'):
            self.get_data_path = (self.output_variable.feature_extractor.
                                  get_data_path)

    def get_data_postfix(self, **kwargs):
        """Get feature postfix (overwrite :py:class:`DataSourceBase`
        implementation).

        :returns: Postfix.
        :rtype: str
        """
        # Get input data postfix
        data_src = self.output_variable.feature_extractor.data_sources[
            self.stage]
        feature_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Add modifier postfix
        if (hasattr(self.output_variable, 'modifier')
                and (self.stage == 'predict')):
            feature_postfix += (self.output_variable.modifier.
                                get_modifier_postfix(**kwargs))

        # Add feature postfix
        feature_postfix += (self.output_variable.feature_extractor.
                            get_feature_extractor_postfix(**kwargs))

        return feature_postfix


class Prediction(OutputVariableDataSourceBase):
    """Prediction data source."""

    def __init__(self, output_variable, **kwargs):
        """Initialize prediction as data source.

        :param output_variable: Output variable to which data is associated.
        :type output_variable: str
        """
        # Build component data source
        name = '{}_{}_prediction'.format(
            output_variable.comp.name, output_variable.name)
        super(Prediction, self).__init__(
            output_variable=output_variable, name=name,
            task_names=None, **kwargs)

    def get_data_postfix(self, **kwargs):
        """Get prediction postfix.

        :returns: Postfix.
        :rtype: str
        """
        return self.output_variable.estimator.get_fit_postfix(**kwargs)


class Output(OutputVariableDataSourceBase):
    """Output data source."""

    def __init__(self, output_variable, **kwargs):
        """Initialize output as data source.

        :param output_variable: Output variable to which data is associated.
        :type output_variable: str
        """
        #: Data-source estimation-stage.
        self.stage = 'output'

        # Build component data source
        name = '{}_{}_{}'.format(
            output_variable.comp.name, output_variable.name, self.stage)
        super(Output, self).__init__(
            output_variable=output_variable, name=name,
            task_names=None, **kwargs)

    def get_data_postfix(self, **kwargs):
        """Get output postfix.

        :returns: Postfix.
        :rtype: str
        """
        # Get input data postfix
        data_src = self.output_variable.output_extractor.data_sources[
            self.stage]
        output_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Add output postfix
        extractor_postfix = (self.output_variable.output_extractor.
                             get_output_extractor_postfix(**kwargs))
        output_postfix = '{}{}'.format(output_postfix, extractor_postfix)

        return output_postfix

    def get_data_path(self, *args, **kwargs):
        """Get data path from base or from original data-source if no
        extraction is performed."""
        if self.output_variable.output_extractor.no_extraction:
            return self.output_variable.output_extractor.data_sources[
                self.stage].get_data_path(*args, **kwargs)
        else:
            return super(Output, self).get_data_path(*args, **kwargs)


def import_module_from_cfg(cfg, name=''):
    """Import actuator module from some container configuration.

    :param cfg: Configuration used to import module of container.
    :param name: Container name. Default is `''`.
    :type cfg: dict
    :type name: str

    :returns: Actuator module.
    :rtype: module
    """
    return (import_module(cfg['module_path'], package=__package__)
            if 'module_path' in cfg else None)
