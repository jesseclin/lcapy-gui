from tkhtmlview import HTMLLabel
from .window import Window


class HelpDialog(Window):

    message = r"""

<h1  style="font-size: 11px;">Editing</h1>

<p style="font-size: 11px;">
Click on the grid to place a red positive cursor then click elsewhere
to place a blue negative cursor.  Then enter c for a capacitor, i for
a current source, l for an inductor, r for a resistor, v for a voltage
source, etc.  Alternatively, use the Components menu.</p>

<p style="font-size: 11px;">
By default, the cursors snap to the grid and align with the other
cursor.  The escape key removes both the positive and negative
cursors.  ctrl+t exchanges the cursors.</p>

<p style="font-size: 11px;">
The attributes of a component (name, value, etc.) can be edited by
right clicking on a component.  Note, voltage and current sources
default to DC.  Select kind as step for transient analysis or specify
the value as a time domain function.</p>

<p style="font-size: 11px;">
The attributes of a node can be edited by right clicking on a
node.  This is useful for defining a ground node.</p>

<h1  style="font-size: 11px;">Analysis</h1>

<p style="font-size: 11px;">
Select a component and use Inspect (ctrl+i) to find the voltage across
a component or the current through a component.  Note the polarity is
defined by the red (plus) and blue (minus) highlighted cursors.</p>

<p style="font-size: 11px;">
Note, voltage and current sources default to DC.  This can be changed
by right clicking on the source and selecting `DC`, `AC`, `step`, or
`arbitrary`.  With `arbitrary`, the value can be an arbitrary
time-domain expression, for example, `4 * H(t) + 2`, where `H(t)` is
the Heaviside step.</p>

<h1  style="font-size: 11px;">Documentation</h1>

<p style="font-size: 11px;">
For further information about Lcapy, see
 <a href="https://lcapy-gui.readthedocs.io"> https://lcapy-gui.readthedocs.io </a>
and  <a href="https://lcapy.readthedocs.io"> https://lcapy.readthedocs.io </a> </p>
"""

    def __init__(self):

        super(HelpDialog, self).__init__(None, None, 'Help!')

        html_label = HTMLLabel(self, html=self.message)
        html_label.pack(fill="both", expand=True)
        html_label.fit_height()
