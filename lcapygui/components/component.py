"""
Defines the components that lcapy-gui can simulate
"""

from numpy import array, sin, cos, pi, dot
from numpy.linalg import norm
import ipycanvas as canvas

from typing import Union
from abc import ABC, abstractmethod


class Component(ABC):

    """
    Describes an lcapy-gui component.
    This is an abstract class, specific components are derived from here.

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the component.
    """

    kinds = {}

    def __init__(self, value: Union[str, int, float]):

        self.name = None
        self.value: str = value
        self.kind = None
        self.nodes = []
        self.initial_value = None
        self.control = None
        self.attrs = ''
        self.opts = []
        self.annotations = []
        self.label = ''
        self.voltage_label = ''
        self.current_label = ''

    @property
    @classmethod
    @abstractmethod
    def TYPE(cls) -> str:
        """
        Component type identifer used by lcapy.
        E.g. Resistors have the identifier R.
        """
        ...

    @property
    @classmethod
    @abstractmethod
    def NAME(cls) -> str:
        """
        The full name of the component.
        E.g. Resistor
        """
        ...

    def __str__(self) -> str:

        return self.TYPE + ' ' + '(%s, %s) (%s, %s)' % \
            (self.nodes[0].position[0], self.nodes[0].position[1],
             self.nodes[1].position[0], self.nodes[1].position[1])

    @abstractmethod
    def __draw_on__(self, editor, layer: canvas.Canvas):
        """
        Handles drawing specific features of components.

        Component end nodes are handled by the draw_on method, which calls this
        abstract method.

        """
        ...

    def length(self) -> float:
        """
        Computes the length of the component.
        """
        return norm(array(self.nodes[1].position)
                    - array(self.nodes[0].position))

    @property
    def midpoint(self) -> array:
        """
        Computes the midpoint of the component.
        """

        return (array(self.nodes[0].position)
                + array(self.nodes[1].position)) / 2

    def along(self) -> array:
        """
        Computes a unit vector pointing along the line of the component.
        If the length of the component is zero, this will return the
        zero vector.
        """
        length = self.length()
        if length == 0:
            return array((0, 0))
        else:
            return (array(self.nodes[1].position)
                    - array(self.nodes[0].position))/length

    def orthog(self) -> array:
        """
        Computes a unit vector pointing anti-clockwise to the line
        of the component.
        """
        delta = self.along()
        theta = pi/2
        rot = array([[cos(theta), -sin(theta)],
                     [sin(theta), cos(theta)]])
        return dot(rot, delta)

    def draw_on(self, editor, layer: canvas.Canvas):
        """
        Draws a single component on a canvas.

        Parameters
        ----------

        editor: Editor
            The editor object to draw on
        layer: Canvas = None
            Layer to draw component on
        """

        # abstract method for drawing components
        self.__draw_on__(editor, layer)

        # node dots
        start = self.nodes[0].position
        end = self.nodes[1].position
        layer.fill_arc(start[0], start[1], editor.STEP // 5, 0, 2 * pi)
        layer.fill_arc(end[0], end[1], editor.STEP // 5, 0, 2 * pi)

    @property
    def vertical(self) -> bool:
        """
        Returns true if component essentially vertical.
        """

        x1, y1 = self.nodes[0].position
        x2, y2 = self.nodes[1].position
        return abs(y2 - y1) > abs(x2 - x1)

    @property
    def label_position(self) -> array:
        """
        Returns position where to place label.   This should be
        customised for each component.
        """

        pos = self.midpoint
        w = 0.75
        if self.vertical:
            pos[0] += w
        else:
            pos[1] += w

        return pos

    def assign_positions(self, x1, y1, x2, y2) -> array:
        """Assign node positions based on cursor positions."""

        return array(((x1, y1), (x2, y2)))