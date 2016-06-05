"""A setting window for The Simple Noteprogram"""

from gettext import gettext as _
from gi.repository import Gtk, Gdk
from the_simple_noteprogram import autostarter, preferences


class _PairFrame(Gtk.Frame):
    """A frame with a grid for adding pairs of labels and widgets
    inside it"""

    def __init__(self, label):
        """Initializes the frame and adds a grid inside it"""
        Gtk.Frame.__init__(self, label=label, border_width=10)
        self._grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL,
                              border_width=10)
        self._grid.set_column_homogeneous(True)
        self.add(self._grid)

    def add_single(self, widget):
        """Adds a widget to the grid"""
        self._grid.add(widget)

    def add_pair(self, description, widget):
        """Adds a label with description as text to the grid and widget
        next to it"""
        # Adding the label into another grid makes it align to left
        minigrid = Gtk.Grid()
        minigrid.add(Gtk.Label(description))
        self._grid.add(minigrid)
        self._grid.attach_next_to(widget, minigrid,
                                  Gtk.PositionType.RIGHT, 1, 1)

    def add_colorbutton(self, description, settingkey):
        """Makes a Gtk.ColorButton, connects it to make it change
        preferences correctly and uses self.add_pair() to add it"""
        rgba = Gdk.RGBA()
        rgba.parse(preferences.get_rgba(settingkey))
        colorb = Gtk.ColorButton.new_with_rgba(rgba)
        colorb.connect('color-set', self._on_color_set, settingkey)
        self.add_pair(description, colorb)

    def add_fontbutton(self, description, settingkey):
        """Makes a Gtk.FontButton, connects it to change preferences
        correctly and uses self.add_pair() to add it"""
        fontb = Gtk.FontButton.new_with_font(preferences.get_font(settingkey))
        fontb.connect('font-set', self._on_font_set, settingkey)
        self.add_pair(description, fontb)

    def _on_color_set(self, colorb, settingkey):
        preferences.set_rgba(settingkey, colorb.get_rgba().to_string())

    def _on_font_set(self, fontb, settingkey):
        preferences.set_font(settingkey, fontb.get_font_name())


class _PreferenceBox(Gtk.Box):

    def __init__(self):
        """Initializes the box and makes the widgets"""
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        # General
        frame = _PairFrame(_("General"))
        button = Gtk.CheckButton(_("Launch this program when I log in"))
        button.set_active(autostarter.get_status())
        button.connect('toggled', self._on_autostart_toggled)
        frame.add_single(button)
        self.add(frame)

        # Colors and fonts
        frame = _PairFrame(_("Notes"))
        frame.add_colorbutton(_("Foreground color"), 'notefg')
        frame.add_colorbutton(_("Background color"), 'notebg')
        frame.add_fontbutton(_("Font"), 'notefont')
        self.add(frame)

    def _on_autostart_toggled(self, button):
        autostarter.set_status(button.get_active())


def run(*ign):
    """Opens up a window for changing the preferences"""
    dialog = Gtk.Dialog(
        # Setting None as the parent is usually a bad idea, but in this
        # case there is no parent window
        _("Preferences"), None, 0,
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    dialog.get_content_area().add(_PreferenceBox())
    dialog.show_all()
    dialog.run()
    dialog.destroy()
