from .component import Component
from numpy import array, sqrt
from numpy.linalg import norm


class Opamp(Component):

    type = "Eopamp"
    sketch_net = 'E 1 2 opamp 3 4'
    sketch_key = 'opamp'
    label_offset = 0
    args = ('Ad', 'Ac', 'Ro')

    # The Nm node is not used (ground).
    node_pinnames = ('out', '', 'in+', 'in-')

    pinname1 = 'in+'
    pinname2 = 'in-'

    hw = 0.85
    hh = 0.85
    bbox_path = ((-hw, -hh), (-hw, hh), (1, 0))

    ppins = {'out': ('rx', 1.25, 0.0),
             'in+': ('lx', -1.25, 0.5),
             'in-': ('lx', -1.25, -0.5),
             'vdd': ('t', 0, 0.5),
             'vdd2': ('t', -0.45, 0.755),
             'vss2': ('b', -0.45, -0.755),
             'vss': ('b', 0, -0.5),
             'ref': ('b', 0.45, -0.245),
             'r+': ('l', -0.85, 0.25),
             'r-': ('l', -0.85, -0.25)}

    npins = {'out': ('rx', 1.25, 0.0),
             'in-': ('lx', -1.25, 0.5),
             'in+': ('lx', -1.25, -0.5),
             'vdd': ('t', 0, 0.5),
             'vdd2': ('t', -0.45, 0.755),
             'vss2': ('b', -0.45, -0.755),
             'vss': ('b', 0, -0.5),
             'ref': ('b', 0.45, -0.245),
             'r-': ('l', -0.85, 0.25),
             'r+': ('l', -0.85, -0.25)}

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    @property
    def pins(self):
        return self.npins if self.mirror else self.ppins

    def draw(self, model, **kwargs):

        sketch = self._sketch_lookup(model)

        kwargs = self.make_kwargs(model, **kwargs)

        tf = self.find_tf(self.pinname1, self.pinname2)

        sketch.draw(model, tf, **kwargs)

    def netitem_nodes(self, node_names):

        parts = []
        for node_name in node_names[0:2]:
            parts.append(node_name)
        parts.append('opamp')
        for node_name in node_names[2:]:
            parts.append(node_name)
        return parts

    @property
    def node1(self):

        return self.nodes[2]

    @property
    def node2(self):

        return self.nodes[3]

    def choose_node_name(self, m, nodes):

        # Handle the special ground node.
        if m == 1:
            return '0'
        return super().choose_node_name(m, nodes)
