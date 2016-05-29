"""The main file"""
import sys
if sys.version_info[:2] < (3, 2):
    sys.exit("This program requires Python 3.2 or newer.")
import argparse
import gettext
import os
import signal
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import about, filepaths, locker


class ArgumentParser(argparse.ArgumentParser):

    def print_help(self):
        print("The Simple Noteprogram")
        print(about.SHORT_DESCRIPTION)
        print()
        argparse.ArgumentParser.print_help(self)

    def error(self, message):
        self.print_help()
        print()
        sys.exit("Error: " + message)


def main(args=None):
    """Runs the program"""
    # Parsing arguments
    parser = ArgumentParser(prog='the-simple-noteprogram')
    parser.add_argument(
        '-v', '--version', action='version',
        help="show the version number and exit",
        version="The Simple Noteprogram " + about.VERSION,
    )
    parser.add_argument(
        '-n', '--new-note', action='store_true',
        help="make a new note",
    )
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    # Checking for another instance
    if locker.duplicatecheck():
        dialog = Gtk.MessageDialog(
            # Setting None as the parent is usually a bad idea, but in
            # this case there is no parent window
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            "The Simple Noteprogram is already running.",
        )
        dialog.run()
        dialog.destroy()
        return

    # Ctrl+C interrupting, doesn't save opened notes
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Internationalization
    gettext.bindtextdomain('the-simple-noteprogram', os.path.join(
        filepaths.prefix, 'share', 'locale',
    ))
    gettext.textdomain('the-simple-noteprogram')

    # These files need to have gettext and icons set up
    from . import indicator, notes

    # Running
    with locker.lockfile():
        if args.new_note:
            notes.new_note()
        Gtk.main()
        notes.unload()

    # This function is not meant to be ran twice
    sys.exit()


if __name__ == '__main__':
    main()
