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

"""A setting manager"""

import configparser
import os
import textwrap
from the_simple_noteprogram import filepaths

_CONFFILES = [
    os.path.join(filepaths.prefix, 'lib', 'the-simple-noteprogram',
                 'preferences.conf'),
    os.path.join(filepaths.user_config_dir, 'preferences.conf'),
]


def set_rgba(key, rgba):
    """Sets an RGBA"""
    _config['Colors'][key] = rgba
    save_and_apply()


def get_rgba(key):
    """Returns an RGBA"""
    return _config['Colors'][key]


def set_font(key, font):
    """Sets a font"""
    _config['Fonts'][key] = font
    save_and_apply()


def get_font(key):
    """Returns a font"""
    return _config['Fonts'][key]


def save_and_apply(*ign):
    """Saves and applies the preferences"""
    comments = ("This file was generated automatically by The Simple "
                "Noteprogram. You may edit it to change the preferences "
                "manually.")
    with open(_CONFFILES[-1], 'w') as f:
        for line in textwrap.wrap(comments, 70):
            print('#', line, file=f)
        f.write('\n')
        _config.write(f)
    for func in _applycommands:
        func()


def add_applycommand(func):
    """Adds a command that save_and_apply will run"""
    if func not in _applycommands:
        _applycommands.append(func)


def remove_applycommand(func):
    """Removes a command added with add_applycommand"""
    if func in _applycommands:
        _applycommands.remove(func)


_applycommands = []

_config = configparser.ConfigParser(dict_type=dict)
_config.read(_CONFFILES)
