"""An about dialog and information about this program"""
from gettext import gettext as _

# Information about authors, add your name here if you've helped with
# making this program but your name is not here yet
AUTHORS = ["Akuli"]
TRANSLATORS = {
    _("Finnish"): "Akuli",
}

# General information
SHORT_DESCRIPTION = "Simple GTK+ 3 application for taking notes"
LONG_DESCRIPTION = "This is a simple note-taking program written in \
Python 3 with GTK+ 3 aimed at GNU/Linux users that displays a note \
icon in the system tray. The tray icon can be clicked and notes with a \
title and a description can be easily made. The notes are always saved \
automatically."
VERSION = '1.0'
KEYWORDS = ["notes", "Gtk+3"]


def about(*ign):
    """Shows an about dialog"""
    # This is not a module-level import because that way this file can
    # be used without having Gtk installed
    from gi.repository import Gtk, GdkPixbuf

    # Loading the logo, defaulting to None
    logo = Gtk.IconTheme.get_default().lookup_icon(
        'the-simple-noteprogram', 48, Gtk.IconLookupFlags.NO_SVG,
    )
    if logo is not None:
        logo = GdkPixbuf.Pixbuf.new_from_file(logo.get_filename())

    # Setting None as the parent is usually a bad idea, but in this case
    # there is no parent window
    dialog = Gtk.AboutDialog(
        program_name="The Simple Noteprogram",
        version=VERSION,
        comments=SHORT_DESCRIPTION,
        license_type=Gtk.License.MIT_X11,
        logo=logo,
        authors=AUTHORS,
        translator_credits="\n".join(
            ": ".join(item) for item in TRANSLATORS.items()
        ),
    )
    dialog.run()
    dialog.destroy()
