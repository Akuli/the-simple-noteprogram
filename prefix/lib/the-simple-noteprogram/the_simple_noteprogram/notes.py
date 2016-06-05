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

"""The notes"""

import functools
from gettext import gettext as _
import os
import re
from gi.repository import Gtk, Gdk, Pango
from the_simple_noteprogram import indicator, filepaths, preferences

_TEMPLATE = 'note-%d.txt'
_REGEX = r'^note-(\d+)\.txt$'
_ALL_NOTES = []


@functools.total_ordering
class _Note(Gtk.Window):
    """A note window"""

    def __init__(self, number, new=False):
        """Reads the note from a file or creates a new note"""
        Gtk.Window.__init__(self)

        # Loading the note
        self._number = int(number)
        if new:
            name = _("Untitled note")
            content = _("Enter notes here...")
        else:
            with open(self._get_path(), 'r') as f:
                name = f.readline().rstrip('\n')
                content = f.read()

        # Creating widgets
        bigbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        smallbox = Gtk.Box()

        entry = self._entry = Gtk.Entry()
        entry.set_tooltip_text(_("The title of the note"))
        entry.connect('changed', self._title_from_entry, True)
        smallbox.pack_start(entry, True, True, 0)
        self.name = name
        self._title_from_entry(entry)

        if hasattr(Gtk.Button, 'new_from_stock'):
            # Gtk.Button.new_from_stock is not deprecated
            button = Gtk.Button.new_from_stock(Gtk.STOCK_REMOVE)
        else:
            button = Gtk.Button(_("Remove"))
        button.set_tooltip_text(_("Remove this note"))
        button.connect('clicked', self.remove)
        smallbox.pack_end(button, False, False, 0)

        bigbox.pack_start(smallbox, False, False, 0)

        textview = self._textview = Gtk.TextView()
        textview.set_tooltip_text(_("The description of the note"))
        textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.content = content
        bigbox.pack_end(textview, True, True, 0)

        self.add(bigbox)
        self.set_default_size(350, 250)
        self.connect('delete-event', self._on_delete_event)
        preferences.add_applycommand(self.apply_settings)
        self.apply_settings()

    def __eq__(self, other):
        """Returns self == other"""
        try:
            return int(self) == int(other)
        except ValueError:
            return False

    def __gt__(self, other):
        """Returns self > other"""
        try:
            return int(self) > int(other)
        except ValueError:
            # Exception chaining tends to make unnecessarily verbose
            # tracebacks
            raise TypeError("cannot compare _Note objects with %r objects"
                            % type(other).__name__) from None

    def __int__(self):
        """Returns the note's number used in the filename and
        ordering"""
        return self._number

    def _get_path(self):
        """Returns the path to the note's file"""
        return os.path.join(filepaths.user_config_dir, _TEMPLATE % self)

    def _on_delete_event(self, window, event):
        """Saves and hides the note, then returns True to make sure the
        window doesn't get destroyed"""
        self.save()
        self.hide()
        return True

    def _title_from_entry(self, entry, update_indicator=False):
        """Updates the window's title"""
        self.set_title(entry.get_text() + " - The Simple Noteprogram")
        if update_indicator:
            indicator.update(_ALL_NOTES)

    @property
    def name(self):
        """Returns the text in the entry"""
        return self._entry.get_text()

    @name.setter
    def name(self, text):
        """Sets text to the entry"""
        self._entry.set_text(text)

    @property
    def content(self):
        """Returns the content in the textview"""
        buf = self._textview.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)

    @content.setter
    def content(self, content):
        """Sets content to the textview"""
        self._textview.get_buffer().set_text(content)

    def show(self, *ign):
        """Shows the note"""
        self.show_all()

    def hide(self, *ign):
        """Hides the note"""
        Gtk.Window.hide(self)

    def save(self, *ign):
        """Saves the note"""
        with open(self._get_path(), 'w') as f:
            f.write(self.name)
            f.write('\n')
            f.write(self.content)

    def remove(self, *ign):
        """Removes the note if the user clicks yes"""
        dialog = Gtk.MessageDialog(
            self, Gtk.DialogFlags.MODAL,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _("Are you sure you want to remove this note?"),
        )
        dialog.set_title(_("Remove note"))
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            # Removing
            preferences.remove_applycommand(self.apply_settings)
            self.hide()
            _ALL_NOTES.remove(self)
            indicator.update(_ALL_NOTES)

            # There is no file if the note has never been saved
            if os.path.isfile(self._get_path()):
                os.remove(self._get_path())

    def apply_settings(self):
        """Applies new color and font preferences"""
        fg = Gdk.RGBA()
        fg.parse(preferences.get_rgba('notefg'))
        bg = Gdk.RGBA()
        bg.parse(preferences.get_rgba('notebg'))
        font = Pango.FontDescription(preferences.get_font('notefont'))

        self._textview.override_color(Gtk.StateFlags.NORMAL, fg)
        self._textview.override_color(Gtk.StateFlags.SELECTED, bg)
        self._textview.override_background_color(Gtk.StateFlags.NORMAL, bg)
        self._textview.override_background_color(Gtk.StateFlags.SELECTED, fg)
        self._textview.override_font(font)


def load():
    """Loads the notes"""
    _ALL_NOTES.clear()
    for name in os.listdir(filepaths.user_config_dir):
        matches = re.search(_REGEX, name)
        path = os.path.join(filepaths.user_config_dir, name)
        if matches and os.path.isfile(path):
            _ALL_NOTES.append(_Note(matches.group(1)))
    _ALL_NOTES.sort()
    indicator.update(_ALL_NOTES)


def unload():
    """Saves and hides the notes"""
    for note in _ALL_NOTES:
        note.save()
        note.hide()


def new_note(*ign):
    """Makes a new note"""
    if _ALL_NOTES:
        number = int(max(_ALL_NOTES)) + 1
    else:
        number = 0
    note = _Note(number, new=True)
    note.show()
    _ALL_NOTES.append(note)
    indicator.update(_ALL_NOTES)
