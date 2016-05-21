"""The main file"""
import sys
if sys.version_info[:2] < (3, 2):
    sys.exit("This program requires Python 3.2 or newer.")
import gettext
import os
import signal
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import filepaths, locker


def main():
    """Runs the program"""
    # Checking for another instance
    if locker.duplicatecheck():
        dialog = Gtk.MessageDialog(
            # Setting None as the parent is usually not a good idea, but
            # in this case there is no parent window
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            "The Simple Noteprogram is already running.",
        )
        dialog.run()
        dialog.destroy()
        return

    # Making sure the icon directory is in GTK's search path
    icondir = os.path.join(filepaths.sharedir, 'icons')
    theme = Gtk.IconTheme.get_default()
    if icondir not in theme.get_search_path():
        theme.append_search_path(icondir)

    # Ctrl+C interrupting, doesn't save opened notes
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Internationalization
    gettext.bindtextdomain('the-simple-noteprogram',
                           os.path.join(filepaths.sharedir, 'locale'))
    gettext.textdomain('the-simple-noteprogram')

    with locker.lockfile():
        from . import indicator, notes
        indicator.load()
        notes.load()
        Gtk.main()
        notes.unload()
        indicator.unload()


if __name__ == '__main__':
    main()
