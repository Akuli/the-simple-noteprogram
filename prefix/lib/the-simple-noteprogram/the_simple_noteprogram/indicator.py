"""The application indicator/tray icon"""
from gettext import gettext as _
from gi.repository import Gtk, Gdk
from . import about

# AppIndicator3 may not be installed
try:
    from gi.repository import AppIndicator3
    _INDICATOR_SUPPORT = True
except ImportError:
    _INDICATOR_SUPPORT = False

# Gtk.StatusIcon is deprecated in new versions of GTK+
if not _INDICATOR_SUPPORT and not hasattr(Gtk, 'StatusIcon'):
    raise ImportError("AppIndicator3 is not installed and Gtk.StatusIcon "
                      "is deprecated in your version of GTK+")


def _on_statusicon_click(statusicon, button, time=None):
    """Runs when the statusicon is clikced"""
    if time is None:
        time = Gtk.get_current_event_time()
    menu.popup(None, None, Gtk.StatusIcon.position_menu,
               statusicon, button, time)


def _new_item(text, command=None, icon=None):
    """Makes a Gtk.MenuItem or Gtk.ImageMenuItem and returns it"""
    if hasattr(Gtk, 'ImageMenuItem') and icon is not None:
        # Gtk.ImageMenuItem is not deprecated in the current version
        # of GTK+
        image = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.MENU)
        item = Gtk.ImageMenuItem(text, image=image)
    else:
        item = Gtk.MenuItem(text)
    if command is not None:
        item.connect('activate', command)
    return item


def update(notelist):
    """Updates the menu, notelist must be in the right order"""
    from .notes import new_note  # notes.py imports this file

    # Clearing the menu
    for item in menu.get_children():
        menu.remove(item)  # this makes a weird error message

    # Adding the menuitems
    menu.add(_new_item(_("New note..."), new_note, Gtk.STOCK_NEW))
    menu.add(Gtk.SeparatorMenuItem())

    if notelist:
        for note in reversed(notelist):  # new notes must be first
            name = note.name
            if len(name) > 50:
                name = name[:50] + "..."
            menu.add(_new_item(name, note.show))
    else:
        item = _new_item(_("(no notes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        menu.add(item)

    menu.add(Gtk.SeparatorMenuItem())
    menu.add(_new_item(_("About..."), about.about, Gtk.STOCK_ABOUT))
    menu.add(_new_item(_("Quit"), Gtk.main_quit, Gtk.STOCK_QUIT))

    # Showing the new items
    menu.show_all()


# Creating the menu and the indicator
menu = Gtk.Menu()

if _INDICATOR_SUPPORT:
    _indicator = AppIndicator3.Indicator.new(
        'the-simple-noteprogram', 'the-simple-noteprogram',
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
    )
    _indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    _indicator.set_menu(menu)
else:
    _indicator = Gtk.StatusIcon()
    _indicator.set_from_icon_name('the-simple-noteprogram')
    _indicator.connect('popup-menu', _on_statusicon_click)
    _indicator.connect('activate', _on_statusicon_click, Gdk.BUTTON_PRIMARY)
