"""The main file"""

import sys
if sys.version_info[:2] < (3, 2):       # NOQA
    sys.exit("This program requires Python 3.2 or newer.")  # NOQA
import argparse
from gettext import gettext as _
import signal
import gi
gi.require_version('Gtk', '3.0')        # NOQA
from gi.repository import Gtk
from the_simple_noteprogram import about, locker, notes


class ArgumentParser(argparse.ArgumentParser):

    def print_help(self):
        from the_simple_noteprogram import about
        print("The Simple Noteprogram: %s." % about.SHORT_DESC)
        print()
        argparse.ArgumentParser.print_help(self)

    def error(self, message):
        self.print_help()
        print()
        sys.exit("Error: " + message)


def main(args=None):
    """Runs the program"""
    # argparse uses gettext, but running 'pygettext *.py' doesn't add
    # argparse's messages to messages.pot
    _("usage: ")
    _("positional arguments")
    _("optional arguments")

    # Parsing arguments
    parser = ArgumentParser(prog='the-simple-noteprogram', add_help=False)
    parser.add_argument('-h', '--help', action='help',
                        help=_("show this help message and exit"))
    parser.add_argument('-v', '--version', action='version',
                        version="The Simple Noteprogram " + about.VERSION,
                        help=_("show the version number and exit"))
    parser.add_argument('-n', '--new-note', action='store_true',
                        help=_("make a new note"))
    args = parser.parse_args(args)

    # Checking for another instance
    if locker.duplicatecheck():
        dialog = Gtk.MessageDialog(
            # Setting None as the parent is usually a bad idea, but in
            # this case there is no parent window
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            _("%s is already running.") % "The Simple Noteprogram",
            title="The Simple Noteprogram",
        )
        dialog.run()
        dialog.destroy()
        sys.exit()

    # Ctrl+C interrupting, doesn't save opened notes
    signal.signal(signal.SIGINT, signal.SIG_DFL)

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
