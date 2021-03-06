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

"""The main file"""

import sys
if sys.version_info[:2] < (3, 2):       # NOQA
    sys.exit("This program requires Python 3.2 or newer.")  # NOQA
import argparse
from gettext import gettext as _
import os
import signal
import filelock
import gi
gi.require_version('Gtk', '3.0')        # NOQA
from gi.repository import Gtk
from the_simple_noteprogram import about, filepaths, indicator, notes


class ArgumentParser(argparse.ArgumentParser):

    def print_help(self):
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

    # Ctrl+C interrupting, doesn't save opened notes
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Running
    lock = filelock.FileLock(os.path.join(filepaths.user_cache_dir, 'lock'))
    try:
        with lock.acquire(timeout=0):
            indicator.load()
            notes.load()
            if args.new_note:
                notes.new_note()
            Gtk.main()
            notes.unload()
    except filelock.Timeout:
        dialog = Gtk.MessageDialog(
            # Setting None as the parent is usually a bad idea, but in
            # this case there is no parent window
            None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
            _("%s is already running.") % "The Simple Noteprogram",
            title="The Simple Noteprogram",
        )
        dialog.run()
        dialog.destroy()

    # This function is not meant to be ran twice
    sys.exit()


if __name__ == '__main__':
    main()
