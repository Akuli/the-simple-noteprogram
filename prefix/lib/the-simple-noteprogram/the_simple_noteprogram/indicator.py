"""The application indicator/tray icon"""

from gettext import gettext as _
from gi.repository import Gtk, Gdk
from the_simple_noteprogram import about, preferences_window

# AppIndicator3 may not be installed
try:
    from gi.repository import AppIndicator3     # NOQA
except ImportError:
    print("AppIndicator3 is not installed.")
    AppIndicator3 = None


# Gtk.StatusIcon is deprecated in new versions of GTK+
if AppIndicator3 is None:
    if not hasattr(Gtk, 'StatusIcon'):
        raise ImportError("AppIndicator3 is not installed and Gtk.StatusIcon "
                          "is deprecated in the current version of GTK+")
    print("AppIndicator3 is not installed, Gtk.StatusIcon "
          "will be used instead")


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
    # This file is imported by notes.py
    from the_simple_noteprogram.notes import new_note

    # Clearing the menu
    for item in menu.get_children():
        menu.remove(item)   # this may make a weird error message

    # Adding the menuitems
    if hasattr(Gtk, 'ImageMenuItem'):
        # Gtk.ImageMenuItem is not deprecated
        new_note_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_NEW)
        pref_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PREFERENCES)
        about_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_ABOUT)
        quit_item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT)
    else:
        new_note_item = Gtk.MenuItem(_("New note"))
        pref_item = Gtk.MenuItem(_("Preferences"))
        about_item = Gtk.MenuItem(_("About"))
        quit_item = Gtk.MenuItem(_("Quit"))

    new_note_item.connect('activate', new_note)
    pref_item.connect('activate', preferences_window.run)
    about_item.connect('activate', about.about)
    quit_item.connect('activate', Gtk.main_quit)

    menu.add(new_note_item)
    menu.add(Gtk.SeparatorMenuItem())
    if notelist:
        for note in reversed(notelist):  # new notes must be first
            name = note.name[:25]
            if len(name) == 25:
                name += "..."
            item = Gtk.MenuItem(name)
            item.connect('activate', note.show)
            menu.add(item)
    else:
        item = _new_item(_("(no notes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        menu.add(item)
    menu.add(Gtk.SeparatorMenuItem())
    menu.add(pref_item)
    menu.add(about_item)
    menu.add(quit_item)

    # Showing the new items
    menu.show_all()


# Creating the menu and the indicator
menu = Gtk.Menu()

_icon = Gtk.IconTheme.get_default().lookup_icon(
    'the-simple-noteprogram', 22,
    Gtk.IconLookupFlags.NO_SVG,
)

if AppIndicator3 is None:
    _indicator = Gtk.StatusIcon()
    _indicator.set_from_file(_icon.get_filename())
    _indicator.connect('popup-menu', _on_statusicon_click)
    _indicator.connect('activate', _on_statusicon_click, Gdk.BUTTON_PRIMARY)
else:
    _indicator = AppIndicator3.Indicator.new(
        'the-simple-noteprogram', _icon.get_filename(),
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
    )
    _indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    _indicator.set_menu(menu)
