"""This file is used to make The Simple Noteprogram start automatically
when the user logs in, based on this:
https://29a.ch/2009/3/17/autostart-autorun-with-python"""

import appdirs
import os
import shutil
from the_simple_noteprogram import filepaths

try:
    import winreg       # NOQA
    _WINDOWS = True
except ImportError:
    _WINDOWS = False


class _RegistryKey:
    """A context manager for opening and closing registry keys easily"""

    def __enter__(self):
        self._key = winreg.OpenKey(
            _registry, r'Software\Microsoft\Windows\CurrentVersion\Run',
            0, winreg.KEY_ALL_ACCESS,
        )
        return self._key

    def __exit__(self, *args):
        winreg.CloseKey(self._key)


def set_status(status):
    """Makes this program run or not run on startup"""
    if _WINDOWS:
        with _RegistryKey() as key:
            if status:
                winreg.SetValueEx(key, "The Simple Noteprogram", 0,
                                  winreg.REG_SZ, filepaths.executable)
            else:
                winreg.DeleteValue(key, "The Simple Noteprogram")
    else:
        if status:
            os.makedirs(os.path.dirname(_desktopdst), exist_ok=True)
            shutil.copy(_desktopsrc, _desktopdst)
        else:
            os.remove(_desktopdst)


def get_status():
    """Checks if the program runs on startup"""
    if _WINDOWS:
        with _RegistryKey() as key:
            try:
                winreg.QueryValueEx(key, "The Simple Noteprogram")
                return True
            except FileNotFoundError:
                return False
    else:
        return os.path.isfile(_desktopdst)


if _WINDOWS:
    _registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
else:
    _desktopsrc = os.path.join(filepaths.prefix, 'share', 'applications',
                               'the-simple-noteprogram.desktop')
    _desktopdst = os.path.join(appdirs.user_config_dir('autostart'),
                               'the-simple-noteprogram.desktop')
