"""This file makes sure only one instance is running at a time"""

import contextlib
import os
import sys
from the_simple_noteprogram import filepaths
try:
    import psutil       # NOQA
except ImportError:
    psutil = None

_LOCKPATH = os.path.join(filepaths.user_cache_dir, 'lock')


def _get_cmdline(pid):
    """This is in a separate function because different versions of
    psutil behave differently"""
    cmdline = psutil.Process(pid).cmdline
    if callable(cmdline):
        # cmdline is a method that returns a list, not a list
        cmdline = cmdline()
    return cmdline


def duplicatecheck():
    """Returns True if another instance is running or False if not"""
    # Reading the file
    try:
        with open(_LOCKPATH, 'r') as f:
            other_pid = int(f.readline())
            other_cmdline = [i for i in f.read().splitlines() if i]
    except (ValueError, UnicodeError, FileNotFoundError):
        # Invalid or no lock file
        return False

    # Checking if psutil is installed
    if psutil is None:
        print("psutil is not installed, cannot check if another instance "
              "of this program is running", file=sys.stderr)
        return False

    # Checking if the process exists and the cmdlines are similar
    try:
        return _get_cmdline(other_pid) == other_cmdline
    except psutil.NoSuchProcess:
        return False


@contextlib.contextmanager
def lockfile():
    """A context manager for creating and removing a lock file"""
    with open(_LOCKPATH, 'w') as f:
        print(_this_pid, file=f)
        for line in _this_cmdline:
            print(line, file=f)
    yield
    os.remove(_LOCKPATH)


_this_pid = os.getpid()
if psutil is not None:
    _this_cmdline = _get_cmdline(_this_pid)
