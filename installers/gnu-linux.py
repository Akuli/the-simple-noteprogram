#!/usr/bin/env python3
"""This script installs The Simple Noteprogram on GNU/Linux operating
systems."""
import sys
if sys.version_info[:2] < (3, 2):
    sys.exit("This program requires Python 3.2 or newer.")
import argparse
import os
from os.path import join
import re
import shutil
import stat
import subprocess


# TODO: platform checks


class ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        self.print_help()
        sys.exit("Error: " + str(message))


parser = ArgumentParser()
parser.add_argument('-p', '--prefix', help="the location to install to")
parser.add_argument('action', help="install or uninstall")
args = parser.parse_args()

if args.prefix is None:
    args.prefix = '/usr/local'  # TODO: sys.prefix or sys.exec_prefix
else:
    args.prefix = os.path.abspath(os.path.expanduser(args.prefix))

if args.action not in ('install', 'uninstall'):
    parser.error("invalid action {!r}".format(args.action))
args.installing = (args.action == 'install')
del args.action

def msg(target):
    print("Installing" if args.installing else "Uninstalling", target + "...")


os.chdir('..')


print("Listing files...")
files = {
    join('data', 'note.glade'):
    join(args.prefix, 'lib', 'the-simple-noteprogram', 'note.glade'),
    join('data', 'gnu-runscript'):
    join(args.prefix, 'bin', 'the-simple-noteprogram'),
}

for name in os.listdir('the_simple_noteprogram'):
    if name != '__pycache__':
        files[join('the_simple_noteprogram', name)] = join(
            args.prefix, 'lib', 'the-simple-noteprogram',
            'the_simple_noteprogram', name,
        )

for lang in os.listdir('locale'):
    mo = join('locale', lang, 'LC_MESSAGES', 'the-simple-noteprogram.mo')
    if os.path.isfile(mo):
        files[mo] = join(args.prefix, 'share', mo)


msg("files")
if args.installing:
    for src, dst in files.items():
        print(" ", src, "->", dst)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
else:
    for dst in files.values():
        print(" ", dst)
        os.remove(dst)


msg("icons")
for name in os.listdir('icons'):
    size = re.search(r'^the-simple-noteprogram-(\d+)\.png$', name).group(1)
    print(" ", "{0}x{0}".format(size))
    if args.installing:
        subprocess.call(['xdg-icon-resource', 'install', '--size', size,
                         join('icons', name), 'the-simple-noteprogram'])
    else:
        subprocess.call(['xdg-icon-resource', 'uninstall', '--size', size,
                         'the-simple-noteprogram'])


msg("the desktop file")
if args.installing:
    subprocess.call(['xdg-desktop-menu', 'install',
                     join('data', 'the-simple-noteprogram.desktop')])
else:
    subprocess.call(['xdg-desktop-menu', 'uninstall',
                     join('data', 'the-simple-noteprogram.desktop')])


# TODO: running script
