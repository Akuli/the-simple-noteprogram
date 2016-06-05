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
SHORT_DESC = _("a simple GTK+ 3 application for taking notes")
LONG_DESC = _("This is a note-taking program written in Python 3 with \
GTK+ 3 aimed mostly at GNU/Linux users. The program displays a note \
icon in the system tray. The tray icon can be clicked and notes with a \
title and a description can be easily made. The notes are always saved \
automatically.")
VERSION = '1.0'
KEYWORDS = ["notes", "Gtk+3"]

# The setup.py needs to do other checks too, because not all
# dependencies can be installed with pip
PIP_DEPENDS = ['appdirs', 'psutil']
# This list is more complete
DEBIAN_DEPENDS = ['gir1.2-gtk-3.0', 'gir1.2-appindicator3-0.1',
                  'python3-gi', 'python3-appdirs', 'python3-psutil']


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
    dialog = Gtk.AboutDialog(
        program_name="The Simple Noteprogram",
        version=VERSION,
        comments=SHORT_DESC[0].upper() + SHORT_DESC[1:],
        logo=logo,
        license=license,
        resizable=True,   # the license is a bit long
        authors=AUTHORS,
        translator_credits="\n".join(
            ": ".join(item) for item in TRANSLATORS.items()
        ),
    )
    dialog.run()
    dialog.destroy()
