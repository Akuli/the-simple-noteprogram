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

"""This file makes sure only one instance is running at a time"""

import contextlib
import os
import sys
from the_simple_noteprogram import filepaths
try:
    import psutil       # NOQA
except ImportError:
    psutil = None

_THIS_PID = os.getpid()
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
            other_cmdline_repr = f.readline().strip()
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
        return repr(_get_cmdline(other_pid)) == other_cmdline_repr
    except psutil.NoSuchProcess:
        return False


@contextlib.contextmanager
def lockfile():
    """A context manager for creating and removing a lock file"""
    with open(_LOCKPATH, 'w') as f:
        print(_THIS_PID, file=f)
        print(repr(_get_cmdline(_THIS_PID)), file=f)
    yield
    os.remove(_LOCKPATH)
