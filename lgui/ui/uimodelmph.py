from .uimodelbase import UIModelBase, Annotation

# In analyze mode could interrogate node voltage with respect to
# ground but need to define a ground node.  Otherwise, could specify a
# pair of cursors (+ and -) and interrogate voltage between them.
# This does not need a ground node defined.  However, would need to
# move the cursors and press a key or button to find the voltage.
# This is not as intuitive as say clicking on a node or clicking on a
# component.  Perhaps clicking on a component would place the cursors
# on its nodes with the positive one as defined in the netlist.


class Cursor:

    def __init__(self, ui, x, y):

        self.layer = ui.cursor_layer
        self.patch = None
        self.x = x
        self.y = y

    @property
    def position(self):

        return self.x, self.y

    def draw(self, color='red', radius=0.5):

        self.patch = self.layer.stroke_filled_circle(self.x, self.y,
                                                     radius,
                                                     color=color,
                                                     alpha=0.5)

    def remove(self):

        self.patch.remove()


class Cursors(list):

    def debug(self):

        s = ''
        for cursor in self:
            s += '%s, %s' % (cursor.x, cursor.y) + '\n'
        return s

    def remove(self):

        while self != []:
            self.pop().remove()


class UIModelMPH(UIModelBase):

    def __init__(self, ui):

        super(UIModelMPH, self).__init__(ui)

        self.cursors = Cursors()
        self.node_cursor = None

    def draw_cursor(self, x, y):

        x, y = self.snap(x, y)

        cursor = Cursor(self.ui, x, y)

        if len(self.cursors) == 0:
            cursor.draw('red')
            self.cursors.append(cursor)

        elif len(self.cursors) == 1:
            cursor.draw('blue')
            self.cursors.append(cursor)

        elif len(self.cursors) == 2:

            rp = (x - self.cursors[0].x)**2 + (y - self.cursors[0].y)**2
            rm = (x - self.cursors[1].x)**2 + (y - self.cursors[1].y)**2

            if rm > rp:
                # Close to plus cursor so add new minus cursor
                self.cursors[1].remove()
                self.cursors[1] = cursor
                self.cursors[1].draw('blue')
            else:
                # Close to minus cursor so change minus cursor to plus cursor
                # and add new minus cursor
                self.cursors[0].remove()
                self.cursors[1].remove()
                self.cursors[0] = self.cursors[1]
                self.cursors[0].draw('red')
                self.cursors[1] = cursor
                self.cursors[1].draw('blue')

        self.ui.refresh()

    def draw_node_select(self, x, y):

        x, y = self.snap(x, y)

        if self.node_cursor is not None:
            self.node_cursor.remove()

        cursor = Cursor(self.ui, x, y)
        cursor.draw('black', 0.2)
        self.node_cursor = cursor
        self.ui.refresh()

    def exception(self, message):
        self.ui.show_info_dialog(message)

    def unselect(self):

        self.cursors.remove()
        self.ui.refresh()

    def on_add_node(self, x, y):

        self.draw_cursor(x, y)
        self.history.add_node(x, y)

    def on_add_cpt(self, cptname):

        if len(self.cursors) < 2:
            # TODO
            return
        x1 = self.cursors[0].x
        y1 = self.cursors[0].y
        x2 = self.cursors[1].x
        y2 = self.cursors[1].y

        self.history.add(cptname, x1, y1, x2, y2)
        self.cpt_add(cptname, x1, y1, x2, y2)

    def on_add_ground(self):

        if self.ground_node is not None:
            # Perhaps could rename old ground?
            self.exception('Ground node already defined')

        if len(self.cursors) == 0:
            return
        cursor = self.cursors[-1]
        x, y = cursor.position
        node = self.nodes.closest(x, y)
        if node is None:
            return
        node.name = '0'

        # TODO: annotate ground

    def on_analyze(self):

        if self.edit_mode:
            self.edit_mode = False
            self.cursors.remove()
            # Indicate in analyze mode.
            if self.components != []:
                self.voltage_annotate(self.components[0])
                self.select(self.components[0])
            self.ui.refresh()

        self.analyze()

    def on_close(self):

        self.ui.quit()

    def on_debug(self):

        s = ''
        s += 'Netlist.........\n'
        s += self.components.as_sch(self.STEP) + '\n'
        s += 'Cursors.........\n'
        s += self.cursors.debug() + '\n'
        s += 'Components......\n'
        s += self.components.debug() + '\n'
        s += 'Nodes...........\n'
        s += self.nodes.debug() + '\n'
        s += 'History.........\n'
        s += self.history.debug() + '\n'
        s += 'Selected.........\n'
        s += str(self.selected) + '\n'
        self.ui.show_message_dialog(s, 'Debug')

    def on_edit(self):

        self.edit_mode = True
        self.voltage_annotations.remove()
        self.ui.refresh()

    def on_export(self):

        filename = self.ui.export_file_dialog(self.filename)
        if filename == '':
            return
        self.export(filename)

    def on_move(self, xshift, yshift):
        self.history.move(xshift, yshift)
        self.move(xshift, yshift)

    def on_rotate(self, angle):
        self.history.rotate(angle)
        self.rotate(angle)

    def on_select(self, x, y):

        cpt = self.components.closest(x, y)
        node = self.nodes.closest(x, y)

        if cpt and node:
            self.ui.show_error(
                'Selected both node %s and cpt %s' % (node, cpt))
            return

        if cpt:
            self.select(cpt)
        elif node:
            self.select(node)
        else:
            self.select(None)

    def on_toggle_mode(self):

        if self.edit_mode:
            self.on_analyze()
        else:
            self.on_edit()

    def on_unselect(self):
        self.history.unselect()
        self.unselect()

    def on_inspect_cpt_admittance(self):
        pass

    def on_inspect_cpt_current(self):

        cpt = self.selected
        self.voltage_annotations.remove()
        self.voltage_annotate(cpt)
        self.show_cpt_current(cpt)

    def on_inspect_cpt_impedance(self):
        pass

    def on_inspect_cpt_voltage(self):

        cpt = self.selected
        self.voltage_annotations.remove()
        self.voltage_annotate(cpt)
        self.show_cpt_voltage(cpt)

    def on_inspect_node_voltage(self):

        gnode = self.ground_node
        if gnode is None:
            self.exception('No ground node defined')

        node = self.selected
        if node is None or self.cpt_selected:
            return

        self.voltage_annotations.remove()

        ann1 = Annotation(self.ui, *node.position, '+')
        self.voltage_annotations.add(ann1)
        ann1.draw(color='red', fontsize=40)

        if gnode is not None:
            ann2 = Annotation(self.ui, *gnode.position, '-')
            self.voltage_annotations.add(ann2)
            ann2.draw(color='blue', fontsize=40)

        self.ui.refresh()

        self.show_node_voltage(node)

    def on_inspect_current(self):

        if not self.selected:
            return
        if self.cpt_selected:
            self.on_inspect_cpt_current()
        # Cannot inspect node current

    def on_inspect_voltage(self):

        if not self.selected:
            return
        if self.cpt_selected:
            self.on_inspect_cpt_voltage()
        else:
            self.on_inspect_node_voltage()

    def on_inspect_admittance(self):

        if not self.selected:
            return
        # TODO

    def on_inspect_impedance(self):

        if not self.selected:
            return
        # TODO

    def on_analyze_key(self, key):

        if key == 'v':
            self.on_inspect_voltage()
        elif key == 'i':
            self.on_inspect_current()
        elif key == 'y':
            self.on_inspect_admittance()
        elif key == 'z':
            self.on_inspect_impedance()

    def on_edit_key(self, key):

        if key == 'ctrl+z':
            self.on_undo()
        elif key == '0':
            self.on_add_ground()
        elif key in ('c', 'i', 'l', 'r', 'v', 'w'):
            self.on_add_cpt(key.upper())

    def on_key(self, key):

        if key == 'ctrl+c':
            self.ui.quit()
        elif key == 'ctrl+d':
            self.on_debug()
        elif key == 'ctrl+h':
            self.on_help()
        elif key == 'ctrl+l':
            self.on_load()
        elif key == 'ctrl+m':
            self.on_toggle_mode()
        elif key == 'ctrl+n':
            self.on_netlist()
        elif key == 'ctrl+s':
            self.on_save()
        elif key == 'ctrl+v':
            self.on_view()
        elif key == 'escape':
            self.on_unselect()
        else:
            if self.edit_mode:
                self.on_edit_key(key)
            else:
                self.on_analyze_key(key)

    def on_left_click(self, x, y):

        self.on_select(x, y)

        if self.edit_mode:
            if self.cpt_selected:
                cpt = self.selected
                if self.ui.debug:
                    print('Selected ' + cpt.cname)
                self.cursors.remove()
                self.draw_cursor(*cpt.nodes[0].position)
                self.draw_cursor(*cpt.nodes[-1].position)
            else:
                if self.ui.debug:
                    print('Add node at (%s, %s)' % (x, y))
                self.on_add_node(x, y)
            return

        # TODO: in future want to be able to edit node attributes as
        # well as place cursor on node.  Perhaps have an inspect mode?
        # The easiest option is to use a different mouse button but
        # this not available in browser implementations.

        if self.cpt_selected:
            self.on_inspect_cpt_voltage()
        else:
            self.draw_node_select(x, y)
            self.on_inspect_node_voltage()

    def on_left_double_click(self, x, y):

        self.on_right_click(x, y)

    def on_load(self):

        filename = self.ui.open_file_dialog()
        if filename == '':
            return
        self.load(filename)
        self.ui.refresh()

    def on_netlist(self):

        netlist = []
        lines = self.circuit().netlist().split('\n')
        for line in lines:
            parts = line.split(';')
            netlist.append(parts[0].strip())
        s = '\n'.join(netlist)
        self.ui.show_message_dialog(s, 'Netlist')

    def on_cpt_changed(self, cpt):

        if not self.edit_mode:
            self.analyze()

    def on_right_click(self, x, y):

        self.on_select(x, y)
        if not self.selected:
            return

        if self.cpt_selected:
            self.ui.show_cpt_properties_dialog(self.selected,
                                               self.on_cpt_changed)
        else:
            self.ui.show_node_properties_dialog(self.selected,
                                                self.on_cpt_changed)

    def on_right_double_click(self, x, y):
        pass

    def on_save(self):

        filename = self.ui.save_file_dialog(self.filename)
        if filename == '':
            return
        self.save(filename)

    def on_undo(self):
        command = self.history.pop()
        print(command)
        # TODO, undo...

    def on_view(self):

        self.view()

    def on_help(self):

        self.ui.show_message_dialog("""
There are two modes: Edit mode and Analyze model.  The default is Edit mode.

In edit mode, click on the grid to place a red positive cursor then
click elsewhere to place a blue negative cursor.  Then enter c for a
capacitor, i for a current source, l for an inductor, r for a
resistor, v for a voltage source, etc.  The escape key will remove the
last defined cursor.

The attributes of a component (name, value, etc.) can be edited by
right clicking on a component.

In analyze mode, left click on a component to display the voltage
across the component.  The polarity is indicated by plus and minus
symbols on the schematic.  The node voltages can be found by clicking
on a node.  This will require a ground node to be defined.  This is
defined in edit mode by typing the 0 key; the ground node is placed at
the negative cursor.""", 'Help')