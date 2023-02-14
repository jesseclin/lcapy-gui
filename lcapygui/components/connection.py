from .component import Component
from numpy import array


class Connection(Component):

    def __init__(self):

        super().__init__(None)

    def __str__(self) -> str:

        return self.TYPE + ' ' + '(%s, %s)' % \
            (self.nodes[0].position[0], self.nodes[0].position[1])

    @property
    def midpoint(self) -> array:
        """
        Computes the midpoint of the component.
        """

        return array(self.nodes[0].position)

    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return 0.5

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), ))