"""Modifier offsetting variable definition."""
import logging
from copy import deepcopy
from ..actuator_base import ModifierBase

#: Logger.
log = logging.getLogger(__name__)


class Actuator(ModifierBase):
    """Modifier offsetting variable"""

    def __init__(self, output_variable, cfg=None, **kwargs):
        """Naming constructor.

        :param output_variable: Output variable to estimate. Default is `None`,
          in which case implementations of this class should set
          :py:attr:`out_var_name`.
        :param cfg: Actuator configuration. Default is `None`.
        :type output_variable: :py:class:`OutputVariable`
        :type cfg: dict
        """
        name = 'offset_variable'
        super(Actuator, self).__init__(
            output_variable=output_variable, name=name, cfg=cfg,
            **kwargs)

        #: Variable to modify.
        self.modified_variable = self.cfg['variable']

        #: Offset to add to the variable.
        self.offset = self.cfg['offset']

    def apply(self, data_src=None, ds=None, **kwargs):
        """Apply modifier to data source.

        :param data_src: Data source to modify. Default is `None`,
          in which case :py:obj:`ds` should be given.
        :param ds: Dataset. Default is `None`,
          in which case :py:obj:`data_src` should be given.
        :type data_src: :py:class:`..data_source.DataSource`
        :type ds: :py:class:`xarray.Dataset`

        :returns: Modified dataset.
        :rtype: Same as :py:obj:`data_src.data`
        """
        if not self.cfg.get('no_verbose'):
            log.info('Adding {} to {}'.format(
                self.offset, self.modified_variable))

        # Copy source dataset (all variables)
        if ds is None:
            try:
                # As xarray.Dataset
                ds = data_src.data.copy(deep=True)
            except TypeError:
                # As dictionary
                ds = deepcopy(data_src.data)

        # Modify variable in dataset
        ds[self.modified_variable] += self.offset

        return ds

    def get_modifier_postfix(self, **kwargs):
        """Get climate modifier postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_offset_{}_{:d}'.format(
            super(Actuator, self).get_modifier_postfix(**kwargs),
            self.modified_variable, int(self.offset * 10 + 0.1))
