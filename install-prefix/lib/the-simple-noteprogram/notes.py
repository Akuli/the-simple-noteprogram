"""The notes"""
import functools
from gettext import gettext as _
import os
from os.path import join
import re
from gi.repository import Gtk
from . import about, indicator, filepaths

TEMPLATE = 'note-{}.txt'
REGEX = r'^note-(\d+)\.txt$'
os.makedirs(join(filepaths.configdir, 'notes'), exist_ok=True)
all_notes = []


@functools.total_ordering
class _Note:
    """A note window"""

    def __init__(self, number, new=False):
        """Reads the note's contents from a file or creates a new note
        if number is None"""
        # Loading the note
        self._number = number
        if new:
            name = _("Untitled note")
            content = _("Enter notes here...")
        else:
            with open(self._get_path(), 'r') as f:
                name = f.readline().rstrip('\n')
                content = f.read()

        # Creating widgets
        gladefile = join(filepaths.libdir, about.DASHES, 'note.glade')
        self._builder = Gtk.Builder()
        self._builder.add_from_file(gladefile)
        get = self._builder.get_object
        get('entry1').set_tooltip_text(_("The title of the note"))
        get('entry1').connect('changed', self._title_from_entry, True)
        self.name = name
        self._title_from_entry(get('entry1'), False)
        get('button1').set_tooltip_text(_("Remove this note"))
        get('button1').connect('clicked', self.remove)
        get('textview1').set_tooltip_text(_("The description of the note"))
        self.content = content
        get('window1').connect('delete-event', self._on_delete_event)

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
            raise TypeError(("cannot compare _Note objects with {.__name__} "
                             "objects").format(type(other))) from None

    def __int__(self):
        """Returns the note's number used in the filename and ordering
        """
        return self._number

    def _get_path(self):
        """Returns the path to the note's file"""
        return join(filepaths.configdir, TEMPLATE.format(int(self)))

    def _on_delete_event(self, window, event):
        """Saves and hides the note, then returns True to make sure the
        window doesn't get partly destroyed"""
        self.save()
        self.hide()
        return True

    def _title_from_entry(self, entry, update_indicator):
        """Updates the window's title"""
        title = entry.get_text() + " - " + about.NAME
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
            self.hide()
            all_notes.remove(self)
            indicator.update(all_notes)

            # The path doesn't exist if the note has never been saved
            path = self._get_path()
            if os.path.isfile(path):
                os.remove(path)


def load():
    """Loads the notes, indicator's load() must be called before this"""
    all_notes.clear()
    for name in os.listdir(filepaths.configdir):
        matches = re.search(REGEX, name)
        if matches and os.path.isfile(join(filepaths.configdir, name)):
            all_notes.append(_Note(int(matches.group(1))))
    all_notes.sort()
    indicator.update(all_notes)


def unload():
    """Saves and hides the notes"""
    for note in all_notes:
        note.save()
        note.hide()


def new_note(*ign):
    """Makes a new note"""
    number = int(max(all_notes)) + 1 if all_notes else 0
    note = _Note(number, new=True)
    note.show()
    all_notes.append(note)
    indicator.update(all_notes)
