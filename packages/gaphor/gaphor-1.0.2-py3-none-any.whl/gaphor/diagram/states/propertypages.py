"""State items property pages.

To register property pages implemented in this module, it is imported in
gaphor.adapter package.
"""

from gi.repository import Gtk

from gaphor.core import _, transactional
from gaphor import UML
from gaphor.diagram.states.transition import TransitionItem
from gaphor.diagram.states.state import StateItem
from gaphor.diagram.propertypages import (
    PropertyPages,
    NamedItemPropertyPage,
    create_hbox_label,
)


@PropertyPages.register(TransitionItem)
class TransitionPropertyPage(NamedItemPropertyPage):
    """Transition property page allows to edit guard specification."""

    def construct(self):
        page = super(TransitionPropertyPage, self).construct()

        subject = self.subject

        if not subject:
            return page

        hbox = create_hbox_label(self, page, _("Guard"))
        entry = Gtk.Entry()
        v = subject.guard.specification
        entry.set_text(v if v else "")
        entry.connect("changed", self._on_guard_change)
        changed_id = entry.connect("changed", self._on_guard_change)
        hbox.pack_start(entry, True, True, 0)

        def handler(event):
            entry.handler_block(changed_id)
            v = event.new_value
            entry.set_text(v if v else "")
            entry.handler_unblock(changed_id)

        self.watcher.watch("guard<Constraint>.specification", handler).subscribe_all()
        entry.connect("destroy", self.watcher.unsubscribe_all)

        return page

    def update(self):
        pass

    @transactional
    def _on_guard_change(self, entry):
        value = entry.get_text().strip()
        self.subject.guard.specification = value


@PropertyPages.register(StateItem)
class StatePropertyPage(NamedItemPropertyPage):
    """State property page."""

    def construct(self):
        page = super(StatePropertyPage, self).construct()

        subject = self.subject

        if not subject:
            return page

        hbox = create_hbox_label(self, page, _("Entry"))
        entry = Gtk.Entry()
        if self.item._entry.subject:
            entry.set_text(self.item._entry.subject.name)
        entry.connect("changed", self._on_text_change, self.item.set_entry)
        hbox.pack_start(entry, True, True, 0)

        hbox = create_hbox_label(self, page, _("Exit"))
        entry = Gtk.Entry()
        if self.item._exit.subject:
            entry.set_text(self.item._exit.subject.name)
        entry.connect("changed", self._on_text_change, self.item.set_exit)
        hbox.pack_start(entry, True, True, 0)

        hbox = create_hbox_label(self, page, _("Do Activity"))
        entry = Gtk.Entry()
        if self.item._do_activity.subject:
            entry.set_text(self.item._do_activity.subject.name)
        entry.connect("changed", self._on_text_change, self.item.set_do_activity)
        hbox.pack_start(entry, True, True, 0)

        page.show_all()

        return page

    def update(self):
        pass

    @transactional
    def _on_text_change(self, entry, method):
        value = entry.get_text().strip()
        method(value)
