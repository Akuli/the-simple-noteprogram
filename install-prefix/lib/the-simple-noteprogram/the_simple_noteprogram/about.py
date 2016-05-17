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
KEYWORDS = ["notes", "Gtk+ 3"]


def about(*ign):
    """Shows an about dialog"""
    # This is not a module-level import because that way this file can
    # be used without having Gtk installed
    from gi.repository import Gtk, GdkPixbuf

    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        Gtk.IconTheme.get_default().lookup_icon(
                'the-simple-noteprogram', 48,
                Gtk.IconLookupFlags.NO_SVG,
            ).get_filename(),
        48, 48,
    )

    # This may result in a warning about setting a transient parent but
    # the application doesn't have any kind of main window to set as the
    # parent
    dialog = Gtk.AboutDialog(
        program_name="The Simple Noteprogram",
        version=VERSION,
        comments=SHORT_DESCRIPTION,
        license_type=Gtk.License.MIT_X11,
        authors=AUTHORS,
        logo=pixbuf,
        translator_credits="\n".join(
            ": ".join(item) for item in TRANSLATORS.items()
        ),
    )
    dialog.run()
    dialog.destroy()
