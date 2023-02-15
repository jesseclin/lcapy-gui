from ...components import Capacitor, Inductor, VCVS, CCVS, VCCS, CCCS
from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class CptPropertiesDialog:

    def __init__(self, ui, cpt, update=None, title=''):

        self.cpt = cpt
        self.update = update

        self.master = Tk()
        self.master.title(title)

        entries = []
        if cpt.kind is not None:
            entries.append(LabelEntry(
                'kind', 'Kind', cpt.kind, list(cpt.kinds.keys()),
                command=self.on_update))

        entries.append(LabelEntry('name', 'Name', cpt.name,
                                  command=self.on_update))
        entries.append(LabelEntry('value', 'Value', cpt.value,
                                  command=self.on_update))

        if isinstance(cpt, Capacitor):
            entries.append(LabelEntry(
                'initial_value', 'v0', cpt.initial_value,
                command=self.on_update))
        elif isinstance(cpt, Inductor):
            entries.append(LabelEntry(
                'initial_value', 'i0', cpt.initial_value,
                command=self.on_update))
        elif isinstance(cpt, (VCVS, VCCS, CCVS, CCCS)):
            names = [c.name for c in ui.model.components if c.name[0] != 'W']
            entries.append(LabelEntry('control', 'Control',
                                      cpt.control, names,
                                      command=self.on_update))

        entries.append(LabelEntry('attrs', 'Attributes', cpt.attrs,
                                  command=self.on_update))

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_update(self, arg=None):

        if self.cpt.kind is not None:
            self.cpt.kind = self.labelentries.get('kind')

        name = self.labelentries.get('name')
        if name.startswith(self.cpt.name[0]):
            self.cpt.name = self.labelentries.get('name')
        else:
            # Cannot change component type.
            pass

        self.cpt.value = self.labelentries.get('value')

        try:
            self.cpt.initial_value = self.labelentries.get('initial_value')
        except KeyError:
            pass

        try:
            self.cpt.control = self.labelentries.get('control')
        except KeyError:
            pass

        self.cpt.attrs = self.labelentries.get('attrs')

        if self.update:
            self.update(self.cpt)

    def on_ok(self):

        self.on_update()

        self.master.destroy()
