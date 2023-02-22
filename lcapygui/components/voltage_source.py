from .component import BipoleComponent


class VoltageSource(BipoleComponent):
    """
    VoltageSource

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the voltage source.
    """

    TYPE = 'V'
    NAME = 'Voltage Source'
    kinds = {'dc': 'DC', 'ac': 'AC', 'step': 'Step', '': 'Arbitrary'}
    default_kind = 'dc'

    @property
    def sketch_net(self):

        return self.TYPE + ' 1 2 ' + self.kind + ' ' + '; right'
