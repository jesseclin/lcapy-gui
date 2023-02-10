
import numpy as np

from typing import Union

from .component import Component


class VCCS(Component):
    """
    VCCS

    Parameters
    ----------

    value: Union[str, int, float]
        The value of the current source.
    """

    TYPE = "G"
    NAME = "VCCS"

    def __init__(self, value: Union[str, int, float]):

        super().__init__(value)

    def __draw_on__(self, editor, layer):

        length = self.length()

        start = self.nodes[0].position
        end = self.nodes[1].position
        mid = 0.5 * self.along() * length + start

        RADIUS = 1.2 * editor.STEP * editor.SCALE
        OFFSET = 0.25 * editor.STEP * editor.SCALE

        # lead 1
        shift = self.along() * RADIUS
        layer.stroke_line(
            start[0], start[1],
            mid[0] - shift[0], mid[1] - shift[1]
        )

        # lead 2
        layer.stroke_line(
            mid[0] + shift[0], mid[1] + shift[1],
            end[0], end[1]
        )

        # diamond
        h_shift = RADIUS * self.orthog()
        v_shift = RADIUS * self.along()

        layer.stroke_line(
            mid[0] + v_shift[0], mid[1] + v_shift[1],
            mid[0] + h_shift[0], mid[1] + h_shift[1]
        )
        layer.stroke_line(
            mid[0] + h_shift[0], mid[1] + h_shift[1],
            mid[0] - v_shift[0], mid[1] - v_shift[1]
        )
        layer.stroke_line(
            mid[0] - v_shift[0], mid[1] - v_shift[1],
            mid[0] - h_shift[0], mid[1] - h_shift[1]
        )
        layer.stroke_line(
            mid[0] - h_shift[0], mid[1] - h_shift[1],
            mid[0] + v_shift[0], mid[1] + v_shift[1]
        )

        # arrow
        offset = (RADIUS - OFFSET) * self.along()
        h_shift = OFFSET * self.orthog()
        v_shift = OFFSET * self.along()

        # line
        layer.stroke_line(
            mid[0] - offset[0], mid[1] - offset[1],
            mid[0] + offset[0], mid[1] + offset[1]
        )

        # arrow head
        layer.stroke_line(
            mid[0] - offset[0], mid[1] - offset[1],
            mid[0] - offset[0] - h_shift[0] + v_shift[0], mid[1] -
            offset[1] - h_shift[1] + v_shift[1]
        )
        layer.stroke_line(
            mid[0] - offset[0], mid[1] - offset[1],
            mid[0] - offset[0] + h_shift[0] + v_shift[0], mid[1] -
            offset[1] + h_shift[1] + v_shift[1]
        )