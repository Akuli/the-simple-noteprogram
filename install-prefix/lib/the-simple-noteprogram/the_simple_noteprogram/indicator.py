"""The application indicator/tray icon"""
from gettext import gettext as _
from gi.repository import AppIndicator3, Gtk
from . import about


class _CustomMenu(Gtk.Menu):
    """Gtk.Menu with some custom methods"""
    # Gtk.ImageMenuItem is deprecated in Gtk 3.10 and newer, it won't be
    # used it if it's not available
    _imagesupport = hasattr(Gtk, 'ImageMenuItem')

    def add_item(self, text, command=None, icon=None):
        """Makes a Gtk.MenuItem, appends it to the menu and then returns
        the item"""
        if self._imagesupport and icon is not None:
            image = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.MENU)
            item = Gtk.ImageMenuItem(text, image=image)
        else:
            item = Gtk.MenuItem(text)
        if command is not None:
            item.connect('activate', command)
        item.show()
        self.add(item)
        return item

    def add_separator(self):
        """Adds and returns a separator"""
        item = Gtk.SeparatorMenuItem()
        item.show()
        self.add(item)
        return item

    def clear(self):
        """Removes all items from the menu"""
        for item in self.get_children():
            self.remove(item)


def load():
    """Shows the indicator"""
    _indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)


def unload():
    """Hides the indicator"""
    _indicator.get_menu().clear()
    _indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)


def update(notelist):
    """Updates the indicator's menu, notelist must be in the right order
    """
    from .notes import new_note  # notes.py imports this file
    menu = _indicator.get_menu()
    menu.clear()
    menu.add_item(_("New note..."), new_note, Gtk.STOCK_NEW)
    menu.add_separator()
    if notelist:
        for note in reversed(notelist):  # new notes must be first
            name = note.name
            if len(name) > 50:
                name = name[:50] + "..."
            menu.add_item(name, note.show)
    else:
        menu.add_item(_("(no notes)")).set_state(Gtk.StateType.INSENSITIVE)
    menu.add_separator()
    menu.add_item(_("About..."), about.about, Gtk.STOCK_ABOUT)
    menu.add_item(_("Quit"), Gtk.main_quit, Gtk.STOCK_QUIT)


# The indicator and menu don't do anything by default so they can be
# made now
_indicator = AppIndicator3.Indicator.new(
    'the-simple-noteprogram',
    Gtk.IconTheme.get_default().lookup_icon(
            'the-simple-noteprogram', 24,
            Gtk.IconLookupFlags.NO_SVG,
        ).get_filename(),
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
)
_indicator.set_menu(_CustomMenu())
