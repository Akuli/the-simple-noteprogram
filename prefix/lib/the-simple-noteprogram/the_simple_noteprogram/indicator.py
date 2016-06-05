# Copyright (c) 2016 Akuli
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""The application _INDICATOR/tray icon"""

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

_MENU = Gtk.Menu()


def _on_statusicon_click(statusicon, button, time=None):
    """Runs when the statusicon is clikced"""
    if time is None:
        time = Gtk.get_current_event_time()
    _MENU.popup(None, None, Gtk.StatusIcon.position_menu,
               statusicon, button, time)


def update(notelist):
    """Updates the menu, notelist must be in the right order"""
    # This file is imported by notes.py
    from the_simple_noteprogram.notes import new_note

    # Clearing the _MENU
    for item in _MENU.get_children():
        _MENU.remove(item)   # this may make a weird error message

    # Making the menuitems
    stocks = [Gtk.STOCK_NEW, Gtk.STOCK_PREFERENCES,
              Gtk.STOCK_HELP, Gtk.STOCK_ABOUT, Gtk.STOCK_QUIT]
    texts = [_("New note"), _("Preferences"),
             _("Help"), _("About"), _("Quit")]
    funcs = [new_note, preferences_window.run,
             about.help, about.about, Gtk.main_quit]

    if hasattr(Gtk, 'ImageMenuItem'):
        # Gtk.ImageMenuItem is not deprecated
        items = [Gtk.ImageMenuItem.new_from_stock(stock) for stock in stocks]
    else:
        items = [Gtk.MenuItem(text) for text in texts]

    for item, func in zip(items, funcs):
        item.connect('activate', func)

    # Adding the menuitems
    _MENU.add(items.pop(0))  # new note
    _MENU.add(Gtk.SeparatorMenuItem())

    if notelist:
        for note in reversed(notelist):     # new notes must be first
            name = note.name[:25]
            if len(name) == 25:
                name += "..."
            item = Gtk.MenuItem(name)
            item.connect('activate', note.show)
            _MENU.add(item)
    else:
        item = Gtk.MenuItem(_("(no notes)"))
        item.set_state(Gtk.StateType.INSENSITIVE)
        _MENU.add(item)
    _MENU.add(Gtk.SeparatorMenuItem())

    for item in items:
        _MENU.add(item)

    _MENU.show_all()


def load():
    """Creates the indicator"""
    global _INDICATOR

    icon = Gtk.IconTheme.get_default().lookup_icon(
        'the-simple-noteprogram', 22,
        Gtk.IconLookupFlags.NO_SVG,
    )

    if AppIndicator3 is None:
        _INDICATOR = Gtk.StatusIcon()
        _INDICATOR.set_from_file(icon.get_filename())
        _INDICATOR.connect('popup-_MENU', _on_statusicon_click)
        _INDICATOR.connect('activate', _on_statusicon_click, Gdk.BUTTON_PRIMARY)
    else:
        _INDICATOR = AppIndicator3.Indicator.new(
            'the-simple-noteprogram', icon.get_filename(),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        _INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        _INDICATOR.set_menu(_MENU)
