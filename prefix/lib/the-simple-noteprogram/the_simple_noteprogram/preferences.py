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


def get_rgba(key):
    """Returns an RGBA"""
    return _config['Colors'][key]


def set_font(key, font):
    """Sets a font"""
    _config['Fonts'][key] = font


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
    if func not in _applycommands:
        _applycommands.append(func)


def remove_applycommand(func):
    if func in _applycommands:
        _applycommands.remove(func)


_applycommands = []

_config = configparser.ConfigParser(dict_type=dict)
print(_config.read(_CONFFILES))
