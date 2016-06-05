"""This file sets up internationalization and icons"""

import gettext
import os
from gi.repository import Gtk
from the_simple_noteprogram import filepaths

# Internationalization
gettext.bindtextdomain('the-simple-noteprogram',
                       os.path.join(filepaths.prefix, 'share', 'locale'))
gettext.textdomain('the-simple-noteprogram')
_ = gettext.gettext

# Icons
theme = Gtk.IconTheme.get_default()
iconpath = os.path.join(filepaths.prefix, 'share', 'icons')
if iconpath not in theme.get_search_path():
    theme.append_search_path(iconpath)
