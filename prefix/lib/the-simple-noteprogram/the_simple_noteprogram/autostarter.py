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

"""This file is used to make The Simple Noteprogram start automatically
when the user logs in, based on this:
https://29a.ch/2009/3/17/autostart-autorun-with-python"""

import os
import shutil
import appdirs
from the_simple_noteprogram import filepaths

try:
    import winreg       # NOQA
    WINDOWS = True
except ImportError:
    WINDOWS = False
    _DESKTOPSRC = os.path.join(filepaths.prefix, 'share', 'applications',
                               'the-simple-noteprogram.desktop')
    _DESKTOPDST = os.path.join(appdirs.user_config_dir('autostart'),
                               'the-simple-noteprogram.desktop')
else:
    _REGISTRY = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)


class _RegistryKey:
    """A context manager for opening and closing registry keys easily"""

    def __enter__(self):
        self._key = winreg.OpenKey(
            _REGISTRY, r'Software\Microsoft\Windows\CurrentVersion\Run',
            0, winreg.KEY_ALL_ACCESS,
        )
        return self._key

    def __exit__(self, *args):
        winreg.CloseKey(self._key)


def set_status(status):
    """Makes this program run or not run on startup"""
    if WINDOWS:
        with _RegistryKey() as key:
            if status:
                winreg.SetValueEx(key, "The Simple Noteprogram", 0,
                                  winreg.REG_SZ, filepaths.executable)
            else:
                winreg.DeleteValue(key, "The Simple Noteprogram")
    else:
        if status:
            os.makedirs(os.path.dirname(_DESKTOPDST), exist_ok=True)
            shutil.copy(_DESKTOPSRC, _DESKTOPDST)
        else:
            os.remove(_DESKTOPDST)


def get_status():
    """Checks if the program runs on startup"""
    if WINDOWS:
        with _RegistryKey() as key:
            try:
                winreg.QueryValueEx(key, "The Simple Noteprogram")
                return True
            except FileNotFoundError:
                return False
    else:
        return os.path.isfile(_DESKTOPDST)
