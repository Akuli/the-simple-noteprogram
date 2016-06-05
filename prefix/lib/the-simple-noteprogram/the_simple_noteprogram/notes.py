"""The notes"""

import functools
from gettext import gettext as _
import os
import re
from gi.repository import Gtk, Gdk, Pango
from the_simple_noteprogram import indicator, filepaths, preferences

_TEMPLATE = 'note-%d.txt'
_REGEX = r'^note-(\d+)\.txt$'


@functools.total_ordering
class _Note:
    """A note window"""

    def __init__(self, number, new=False):
        """Reads the note from a file or creates a new note"""
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
        self._builder = Gtk.Builder()
        self._builder.add_from_file(os.path.join(
            filepaths.prefix, 'lib',
            'the-simple-noteprogram', 'note.glade',
        ))
        get = self._builder.get_object
        get('entry1').set_tooltip_text(_("The title of the note"))
        get('entry1').connect('changed', self._title_from_entry, True)
        self.name = name
        self._title_from_entry(get('entry1'), False)
        get('button1').set_tooltip_text(_("Remove this note"))
        get('button1').connect('clicked', self.remove)
        get('textview1').set_tooltip_text(_("The description of the note"))
        get('textview1').set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.content = content
        get('window1').connect('delete-event', self._on_delete_event)

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

    def _title_from_entry(self, entry, update_indicator):
        """Updates the window's title"""
        title = entry.get_text() + " - The Simple Noteprogram"
        self._builder.get_object('window1').set_title(title)
        if update_indicator:
            indicator.update(all_notes)

    @property
    def name(self):
        """Returns the text in the entry"""
        return self._builder.get_object('entry1').get_text()

    @name.setter
    def name(self, text):
        """Sets text to the entry"""
        self._builder.get_object('entry1').set_text(text)

    @property
    def content(self):
        """Returns the content in the textview"""
        buf = self._builder.get_object('textview1').get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)

    @content.setter
    def content(self, content):
        """Sets content to the textview"""
        self._builder.get_object('textview1').get_buffer().set_text(content)

    def show(self, *ign):
        """Shows the note"""
        self._builder.get_object('window1').show_all()

    def hide(self, *ign):
        """Hides the note"""
        self._builder.get_object('window1').hide()

    def save(self, *ign):
        """Saves the note"""
        with open(self._get_path(), 'w') as f:
            f.write(self.name)
            f.write('\n')
            f.write(self.content)

    def remove(self, *ign):
        """Removes the note if the user clicks yes"""
        dialog = Gtk.MessageDialog(
            self._builder.get_object('window1'), Gtk.DialogFlags.MODAL,
            Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO,
            _("Are you sure you want to remove this note?"),
            title=_("Remove note"),
        )
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            # Removing
            preferences.remove_applycommand(self.apply_settings)
            self.hide()
            all_notes.remove(self)
            indicator.update(all_notes)

            # There is no file if the note has never been saved
            if os.path.isfile(self._get_path()):
                os.remove(self._get_path())

    def apply_settings(self):
        """Applies new color and font preferences"""
        textview = self._builder.get_object('textview1')

        fg = Gdk.RGBA()
        fg.parse(preferences.get_rgba('notefg'))
        bg = Gdk.RGBA()
        bg.parse(preferences.get_rgba('notebg'))
        font = Pango.FontDescription(preferences.get_font('notefont'))

        textview.override_color(Gtk.StateFlags.NORMAL, fg)
        textview.override_color(Gtk.StateFlags.SELECTED, bg)
        textview.override_background_color(Gtk.StateFlags.NORMAL, bg)
        textview.override_background_color(Gtk.StateFlags.SELECTED, fg)
        textview.override_font(font)


def unload():
    """Saves and hides the notes"""
    for note in all_notes:
        note.save()
        note.hide()


def new_note(*ign):
    """Makes a new note"""
    if all_notes:
        number = int(max(all_notes)) + 1
    else:
        number = 0
    note = _Note(number, new=True)
    note.show()
    all_notes.append(note)
    indicator.update(all_notes)


# Loading the notes
all_notes = []
for name in os.listdir(filepaths.user_config_dir):
    path = os.path.join(filepaths.user_config_dir, name)
    matches = re.search(_REGEX, name)
    if matches and os.path.isfile(path):
        all_notes.append(_Note(matches.group(1)))
all_notes.sort()

indicator.update(all_notes)
