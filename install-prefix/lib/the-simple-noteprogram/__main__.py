"""The main file"""
import sys
if sys.version_info[:2] < (3, 2):                           # NOQA
    sys.exit("This program requires Python 3.2 or newer.")  # NOQA
import gettext
from os.path import join
import signal
import gi
gi.require_version('Gtk', '3.0')                            # NOQA
gi.require_version('AppIndicator3', '0.1')                  # NOQA
from gi.repository import Gtk
from . import about, filepaths


# Internationalization
gettext.bindtextdomain(
    about.DASHES, localedir=join(filepaths.sharedir, 'locale'),
)
gettext.textdomain(about.DASHES)

# The icon directory is probably not in Gtk.IconTheme's search_path
theme = Gtk.IconTheme.get_default()
if join(filepaths.sharedir, 'icons') not in theme.get_search_path():
    theme.append_search_path(join(filepaths.sharedir, 'icons'))

# Ctrl+C interrupting, doesn't save currently opened notes
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    """Runs the program"""
    from . import indicator, notes
    indicator.load()
    notes.load()
    Gtk.main()
    notes.unload()
    indicator.unload()

if __name__ == '__main__':
    main()
