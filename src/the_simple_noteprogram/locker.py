"""This file makes sure only one instance is running at a time"""
import contextlib
import os
import tempfile
import psutil

LOCKPATH = os.path.join(tempfile.gettempdir(), 'the-simple-noteprogram-lock')


def duplicatecheck():
    """Returns True if another instance is running or False if not using
    a lockfile"""
    try:
        with open(LOCKPATH, 'rb') as f:
            pid = int(f.read())
    except (FileNotFoundError, ValueError):
        # Invalid or no pid file
        return False
    return os.getpid() != pid and psutil.pid_exists(pid)


@contextlib.contextmanager
def lockfile():
    """A context manager for creating and removing a lock file"""
    with open(LOCKPATH, 'w') as f:
        print(os.getpid(), file=f)
    yield
    os.remove(LOCKPATH)
