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

"""An about dialog and information about this program"""

from gettext import gettext as _
import os

# Information about authors, add your name here if you've helped with
# making this program but your name is not here yet
AUTHORS = ["Akuli"]
TRANSLATORS = {
    _("Finnish"): "Akuli",
}

# General information
SHORT_DESC = _("a simple application for taking notes")
LONG_DESC = _("This program displays a note icon in the system tray. \
The tray icon can be clicked and notes with a title and a description \
can be easily made. The notes are always saved automatically.")
VERSION = '1.0-beta'
KEYWORDS = ["notes", "Gtk+3"]

# The setup.py needs to do other checks too, because not all
# dependencies can be installed with pip
PIP_DEPENDS = ['appdirs', 'psutil']
# This list is more complete
DEBIAN_DEPENDS = ['gir1.2-gtk-3.0', 'gir1.2-appindicator3-0.1',
                  'python3-gi', 'python3-appdirs', 'python3-psutil']


def help(*ign):
    """Shows a help dialog"""
    # This is not a module-level import because that way this file can
    # be used without having Gtk installed
    from gi.repository import Gtk

    dialog = Gtk.MessageDialog(
        # Leaving the transient parent to None is usually a bad idea,
        # but in this case there is no parent window
        None, 0, Gtk.MessageType.QUESTION,    # a questionmark icon
        Gtk.ButtonsType.OK, LONG_DESC,
    )
    dialog.set_title(_("Help"))
    dialog.run()
    dialog.destroy()


def about(*ign):
    """Shows an about dialog"""
    # This is not a module-level import because that way this file can
    # be used without having Gtk installed
    from gi.repository import Gtk, GdkPixbuf
    from the_simple_noteprogram import filepaths

    # Loading the license
    licensefile = os.path.join(filepaths.prefix, 'lib',
                               'the-simple-noteprogram', 'LICENSE')
    with open(licensefile, 'r') as f:
        license = f.read()

    # Loading the logo
    logo = Gtk.IconTheme.get_default().lookup_icon(
        'the-simple-noteprogram', 48, Gtk.IconLookupFlags.NO_SVG,
    )
    logo = GdkPixbuf.Pixbuf.new_from_file(logo.get_filename())

    # Leaving the transient parent to None is usually a bad idea, but in
    # this case there is no parent window
    dialog = Gtk.AboutDialog()
    dialog.set_program_name("The Simple Noteprogram")
    dialog.set_version(VERSION)
    dialog.set_comments(SHORT_DESC[0].upper() + SHORT_DESC[1:])
    dialog.set_logo(logo)
    dialog.set_license(license)
    dialog.set_resizable(True)      # the license is a bit long
    dialog.set_authors(AUTHORS)
    dialog.set_translator_credits(
        "\n".join(": ".join(item) for item in TRANSLATORS.items())
    )
    dialog.run()
    dialog.destroy()
