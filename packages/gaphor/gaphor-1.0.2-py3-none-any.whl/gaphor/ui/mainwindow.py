"""
The main application window.
"""

import logging
import os.path

import importlib.resources
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Gtk

from gaphor import UML, Application
from gaphor.UML.event import ModelFactoryEvent
from gaphor.core import (
    _,
    event_handler,
    action,
    toggle_action,
    build_action_group,
    transactional,
)
from gaphor.abc import Service, ActionProvider
from gaphor.UML.event import AttributeChangeEvent, FlushFactoryEvent
from gaphor.services.undomanager import UndoManagerStateChanged
from gaphor.ui.abc import UIComponent
from gaphor.ui.accelmap import load_accel_map, save_accel_map
from gaphor.ui.diagrampage import DiagramPage
from gaphor.ui.event import DiagramPageChange, DiagramShow, FilenameChanged, WindowClose
from gaphor.ui.layout import deserialize
from gaphor.ui.namespace import Namespace
from gaphor.ui.toolbox import Toolbox


log = logging.getLogger(__name__)

ICONS = (
    "gaphor-24x24.png",
    "gaphor-48x48.png",
    "gaphor-96x96.png",
    "gaphor-256x256.png",
)


class MainWindow(Service, ActionProvider):
    """
    The main window for the application.
    It contains a Namespace-based tree view and a menu and a statusbar.
    """

    size = property(lambda s: s.properties.get("ui.window-size", (760, 580)))
    resizable = True

    menu_xml = """
      <ui>
      </ui>
    """

    def __init__(
        self,
        event_manager,
        component_registry,
        element_factory,
        action_manager,
        properties,
    ):
        self.event_manager = event_manager
        self.component_registry = component_registry
        self.element_factory = element_factory
        self.action_manager = action_manager
        self.properties = properties

        self.title = "Gaphor"
        self.window = None
        self.filename = None
        self.model_changed = False
        self.layout = None

        self.init_styling()
        self.init_action_group()

    def init_styling(self):
        with importlib.resources.path("gaphor.ui", "layout.css") as css_file:
            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(str(css_file))
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

    def shutdown(self):
        if self.window:
            self.window.destroy()
            self.window = None
        save_accel_map()

        em = self.event_manager
        em.unsubscribe(self._on_file_manager_state_changed)
        em.unsubscribe(self._on_undo_manager_state_changed)
        em.unsubscribe(self._new_model_content)

    def init_action_group(self):
        self.action_group = build_action_group(self)
        for name, label in (
            ("file", "_File"),
            ("file-export", "_Export"),
            ("file-import", "_Import"),
            ("edit", "_Edit"),
            ("diagram", "_Diagram"),
            ("tools", "_Tools"),
            ("help", "_Help"),
        ):
            a = Gtk.Action.new(name, label, None, None)
            a.set_property("hide-if-empty", False)
            self.action_group.add_action(a)

        self.action_manager.register_action_provider(self)

    def get_ui_component(self, name):
        return self.component_registry.get(UIComponent, name)

    def open(self, gtk_app=None):
        """Open the main window.
        """
        load_accel_map()

        self.window = (
            Gtk.ApplicationWindow.new(gtk_app)
            if gtk_app
            else Gtk.Window.new(type=Gtk.WindowType.TOPLEVEL)
        )
        self.window.set_title(self.title)
        self.window.set_default_size(*self.size)

        # set default icons of gaphor windows
        with importlib.resources.path("gaphor.ui", "pixmaps") as icon_dir:
            icons = (
                GdkPixbuf.Pixbuf.new_from_file(os.path.join(icon_dir, f)) for f in ICONS
            )
            self.window.set_icon_list(list(icons))

        self.window.add_accel_group(self.action_manager.get_accel_group())

        # Create a full featured window.
        vbox = Gtk.VBox()
        self.window.add(vbox)
        vbox.show()

        menubar = self.action_manager.get_widget(self.action_manager.menubar_path)
        if menubar:
            vbox.pack_start(menubar, False, True, 0)

        toolbar = self.action_manager.get_widget(self.action_manager.toolbar_path)
        if toolbar:
            vbox.pack_start(toolbar, False, True, 0)

        def _factory(name):
            comp = self.get_ui_component(name)
            log.debug("open component %s" % str(comp))
            return comp.open()

        self.layout = []

        with importlib.resources.open_text("gaphor.ui", "layout.xml") as f:
            deserialize(self.layout, vbox, f.read(), _factory)

        vbox.show()
        # TODO: add statusbar

        self.window.present()

        self.window.connect("delete-event", self._on_window_delete)

        # We want to store the window size, so it can be reloaded on startup
        self.window.set_resizable(True)
        self.window.connect("size-allocate", self._on_window_size_allocate)

        em = self.event_manager
        em.subscribe(self._on_file_manager_state_changed)
        em.subscribe(self._on_undo_manager_state_changed)
        em.subscribe(self._new_model_content)

    def open_welcome_page(self):
        """
        Create a new tab with a textual welcome page, a sort of 101 for
        Gaphor.
        """
        pass

    def set_title(self):
        """
        Sets the window title.
        """
        if self.window:
            if self.filename:
                title = "%s - %s" % (self.title, self.filename)
            else:
                title = self.title
            if self.model_changed:
                title += " *"
            self.window.set_title(title)

    # Signal callbacks:

    @event_handler(ModelFactoryEvent)
    def _new_model_content(self, event):
        """
        Open the toplevel element and load toplevel diagrams.
        """
        # TODO: Make handlers for ModelFactoryEvent from within the GUI obj
        for diagram in self.element_factory.select(
            lambda e: e.isKindOf(UML.Diagram)
            and not (e.namespace and e.namespace.namespace)
        ):
            self.event_manager.handle(DiagramShow(diagram))

    @event_handler(FilenameChanged)
    def _on_file_manager_state_changed(self, event):
        self.model_changed = False
        self.filename = event.filename
        self.set_title()

    @event_handler(UndoManagerStateChanged)
    def _on_undo_manager_state_changed(self, event):
        """
        """
        undo_manager = event.service
        if self.model_changed != undo_manager.can_undo():
            self.model_changed = undo_manager.can_undo()
            self.set_title()

    def _on_window_delete(self, window=None, event=None):
        self.event_manager.handle(WindowClose(self))
        return True

    def _on_window_size_allocate(self, window, allocation):
        """
        Store the window size in a property.
        """
        self.properties.set("ui.window-size", (allocation.width, allocation.height))

    def quit(self):
        Application.quit()

    # TODO: Does not belong here
    def create_item(self, ui_component):
        """
        Create an item for a ui component. This method can be called from UIComponents.
        """
        window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
        window.set_transient_for(self.window)
        window.set_title(ui_component.title)
        window.add(ui_component.open())
        window.show()
        window.ui_component = ui_component


Gtk.AccelMap.add_filter("gaphor")


class Diagrams(UIComponent, ActionProvider):

    title = _("Diagrams")
    placement = ("left", "diagrams")

    menu_xml = """
      <ui>
        <menubar name="mainwindow">
          <menu action="diagram">
            <separator/>
            <menuitem action="diagram-drawing-style" />
            <separator/>
          </menu>
        </menubar>
      </ui>
    """

    def __init__(self, event_manager, element_factory, action_manager, properties):
        self.event_manager = event_manager
        self.element_factory = element_factory
        self.action_manager = action_manager
        self.properties = properties
        self._notebook = None
        self.action_group = build_action_group(self)
        self.action_group.get_action("diagram-drawing-style").set_active(
            self.properties("diagram.sloppiness", 0) != 0
        )
        self._page_ui_settings = None

    def open(self):
        """Open the diagrams component.

        Returns:
            The Gtk.Notebook.
        """

        self._notebook = Gtk.Notebook()
        self._notebook.show()
        self._notebook.connect("switch-page", self._on_switch_page)
        self.event_manager.subscribe(self._on_show_diagram)
        self.event_manager.subscribe(self._on_name_change)
        self.event_manager.subscribe(self._on_flush_model)
        return self._notebook

    def close(self):
        """Close the diagrams component."""

        self.event_manager.unsubscribe(self._on_flush_model)
        self.event_manager.unsubscribe(self._on_name_change)
        self.event_manager.unsubscribe(self._on_show_diagram)
        if self._notebook:
            self._notebook.destroy()
            self._notebook = None

    def get_current_diagram(self):
        """Returns the current page of the notebook.

        Returns (DiagramPage): The current diagram page.
        """

        page_num = self._notebook.get_current_page()
        child_widget = self._notebook.get_nth_page(page_num)
        if child_widget is not None:
            return child_widget.diagram_page.get_diagram()
        else:
            return None

    def get_current_view(self):
        """Returns the current view of the diagram page.

        Returns (GtkView): The current view.
        """
        if not self._notebook:
            return
        page_num = self._notebook.get_current_page()
        child_widget = self._notebook.get_nth_page(page_num)
        return child_widget.diagram_page.get_view()

    def cb_close_tab(self, button, widget):
        """Callback to close the tab and remove the notebook page.

        Args:
            button (Gtk.Button): The button the callback is from.
            widget (Gtk.Widget): The child widget of the tab.
        """

        page_num = self._notebook.page_num(widget)
        # TODO why does Gtk.Notebook give a GTK-CRITICAL if you remove a page
        #   with set_show_tabs(True)?
        self._clear_ui_settings()
        self._notebook.remove_page(page_num)
        widget.diagram_page.close()
        widget.destroy()

    def create_tab(self, title, widget):
        """Creates a new Notebook tab with a label and close button.

        Args:
            title (str): The title of the tab, the diagram name.
            widget (Gtk.Widget): The child widget of the tab.
        """

        page_num = self._notebook.append_page(
            child=widget, tab_label=self.tab_label(title, widget)
        )
        self._notebook.set_current_page(page_num)
        self._notebook.set_tab_reorderable(widget, True)

        self.event_manager.handle(DiagramPageChange(widget))
        self._notebook.set_show_tabs(True)

    def tab_label(self, title, widget):
        tab_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        label = Gtk.Label(label=title)
        tab_box.pack_start(child=label, expand=True, fill=True, padding=0)

        close_image = Gtk.Image.new_from_icon_name(
            icon_name="window-close", size=Gtk.IconSize.MENU
        )
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.set_focus_on_click(False)
        button.add(close_image)
        button.connect("clicked", self.cb_close_tab, widget)
        tab_box.pack_start(child=button, expand=False, fill=False, padding=0)
        tab_box.show_all()
        return tab_box

    def get_widgets_on_pages(self):
        """Gets the widget on each open page Notebook page.

        The page is the page number in the Notebook (0 indexed) and the widget
        is the child widget on each page.

        Returns:
            List of tuples (page, widget) of the currently open Notebook pages.
        """

        widgets_on_pages = []
        if not self._notebook:
            return widgets_on_pages

        num_pages = self._notebook.get_n_pages()
        for page in range(0, num_pages):
            widget = self._notebook.get_nth_page(page)
            widgets_on_pages.append((page, widget))
        return widgets_on_pages

    def _on_switch_page(self, notebook, page, page_num):
        self._clear_ui_settings()
        self._add_ui_settings(page_num)
        self.event_manager.handle(DiagramPageChange(page))

    def _add_ui_settings(self, page_num):
        action_manager = self.action_manager
        child_widget = self._notebook.get_nth_page(page_num)
        self.action_manager.register_action_provider(child_widget.diagram_page)
        self._page_ui_settings = child_widget.diagram_page

    def _clear_ui_settings(self):
        # TODO: notebook.get_current_page()?
        if self._page_ui_settings:
            self.action_manager.unregister_action_provider(self._page_ui_settings)
            self._page_ui_settings = None

    @event_handler(DiagramShow)
    def _on_show_diagram(self, event):
        """Show a Diagram element in the Notebook.

        If a diagram is already open on a Notebook page, show that one,
        otherwise create a new Notebook page.

        Args:
            event: The service event that is calling the method.
        """

        diagram = event.diagram

        # Try to find an existing diagram page and give it focus
        for page, widget in self.get_widgets_on_pages():
            if widget.diagram_page.get_diagram() is diagram:
                self._notebook.set_current_page(page)
                return widget.diagram_page

        # No existing diagram page found, creating one
        page = DiagramPage(
            diagram, self.event_manager, self.element_factory, self.properties
        )
        widget = page.construct()
        try:
            widget.set_css_name("diagram-tab")
        except AttributeError:
            pass  # Gtk.Widget.set_css_name() is added in 3.20
        widget.set_name("diagram-tab")
        widget.diagram_page = page
        page.set_drawing_style(self.properties("diagram.sloppiness", 0))

        self.create_tab(diagram.name, widget)
        return page

    @event_handler(FlushFactoryEvent)
    def _on_flush_model(self, event):
        """
        Close all tabs.
        """
        while self._notebook.get_n_pages():
            self._notebook.remove_page(0)

    @event_handler(AttributeChangeEvent)
    def _on_name_change(self, event):
        if event.property is UML.Diagram.name:
            for page in range(0, self._notebook.get_n_pages()):
                widget = self._notebook.get_nth_page(page)
                if event.element is widget.diagram_page.diagram:
                    self._notebook.set_tab_label(
                        widget, self.tab_label(event.new_value, widget)
                    )

    @toggle_action(name="diagram-drawing-style", label="Hand drawn style", active=False)
    def hand_drawn_style(self, active):
        """Toggle between straight diagrams and "hand drawn" diagram style."""

        if active:
            sloppiness = 0.5
        else:
            sloppiness = 0.0
        for page, widget in self.get_widgets_on_pages():
            widget.diagram_page.set_drawing_style(sloppiness)
        self.properties.set("diagram.sloppiness", sloppiness)
