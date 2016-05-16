"""An about dialog and information about this program"""
from gettext import gettext as _

# Information about authors, add your name here if you've helped with
# making this program but your name is not here yet
AUTHORS = ["Akuli"]
TRANSLATORS = {
    _("Finnish"): "Akuli",
}

# General information
NAME = "The Simple Noteprogram"
DASHES = 'the-simple-noteprogram'
SCORES = 'the_simple_noteprogram'
SHORT_DESCRIPTION = "Simple GTK+ 3 application for taking notes"
# TODO: fix this
LONG_DESCRIPTION = """\
blah blah blah
"""
VERSION = '1.0'
KEYWORDS = ["notes", "Gtk+ 3"]


def about(*ign):
    """Shows an about dialog"""
    # This is not a module-level import because that way this file can
    # be used without having Gtk installed
    from gi.repository import Gtk, GdkPixbuf

    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
        Gtk.IconTheme.get_default().lookup_icon(
                DASHES,
                48,
                Gtk.IconLookupFlags.NO_SVG,
            ).get_filename(),
        48,
        48,
    )

    # This may result in a warning about setting a transient parent but
    # the application doesn't have any kind of main window to set as the
    # parent
    dialog = Gtk.AboutDialog(
        program_name=NAME,
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