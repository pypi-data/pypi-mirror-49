"""
State transition implementation.
"""

from gaphor import UML
from gaphor.diagram.diagramline import NamedLine
from gaphor.diagram.style import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_TOP


class TransitionItem(NamedLine):
    """
    Representation of state transition.
    """

    __uml__ = UML.Transition

    __style__ = {"name-align": (ALIGN_RIGHT, ALIGN_TOP), "name-padding": (5, 15, 5, 5)}

    def __init__(self, id=None, model=None):
        NamedLine.__init__(self, id, model)
        self._guard = self.add_text("guard.specification", editable=True)
        self.watch("subject<Transition>.guard<Constraint>.specification", self.on_guard)

    def postload(self):
        """
        Load guard specification information.
        """
        try:
            self._guard.text = self.subject.guard.specification or ""
        except AttributeError:
            self._guard.text = ""
        super(TransitionItem, self).postload()

    def on_guard(self, event):
        try:
            self._guard.text = self.subject.guard.specification or ""
        except AttributeError:
            self._guard.text = ""
        self.request_update()

    def draw_tail(self, context):
        cr = context.cairo
        cr.line_to(0, 0)
        cr.stroke()
        cr.move_to(15, -6)
        cr.line_to(0, 0)
        cr.line_to(15, 6)
