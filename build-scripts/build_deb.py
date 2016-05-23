#!/usr/bin/env python3
"""This file builds a Debian package of The Simple Noteprogram."""
import sys
if sys.version_info[:2] < (3, 2):                           # NOQA
    sys.exit("This script requires Python 3.2 or newer.")   # NOQA
import fnmatch
import hashlib
import math
import os
from os.path import abspath, dirname, join
import re
import shutil
import subprocess
import textwrap


# Some settings
IGNORED = [
    'src/the_simple_noteprogram/__pycache__/*',
    'src/data/*-launcher',
    'src/data/*.desktop',
    'src/icons/*',
    'src/locale/*/LC_MESSAGES/the-simple-noteprogram.po',
]


# Platform checks
def platform_check(requirement, assertion):
    if not assertion:
        sys.exit("This script requires {}.".format(requirement))

platform_check(
    "an operating system that uses / as the path separator, . as the "
    "current directory and .. as the parent directory",
    (os.path.sep, os.path.curdir, os.path.pardir) == ('/', '.', '..'))
platform_check("an operating system with a root account", hasattr(os, 'getuid'))
platform_check("root access", os.getuid() == 0)


# Importing about.py, this is bad but not too bad for this script
sys.path.append(join(dirname(dirname(abspath(__file__))), 'src'))
from the_simple_noteprogram import about  # NOQA


os.chdir(dirname(dirname(abspath(__file__))))


# Cleaning
if os.path.isdir('build'):
    shutil.rmtree('build')


# Listing files
FILES = {
    'src/data/gnu-linux-launcher':
    'usr/bin/the-simple-noteprogram',

    'src/data/the-simple-noteprogram.desktop':
    'usr/share/applications/the-simple-noteprogram.desktop',
}

for root, dirs, files in os.walk('src'):
    for f in files:
        f = join(root, f)
        if not any(fnmatch.fnmatch(f, i) for i in IGNORED):
            FILES[f] = join('usr/lib/the-simple-noteprogram',
                            f.partition('src/')[2])

dsttemplate = 'usr/share/icons/hicolor/{0}x{0}/apps/the-simple-noteprogram.png'
for i in os.listdir('src/icons'):
    number = re.match(r'^the-simple-noteprogram-(\d+).png$', i).group(1)
    FILES[join('src/icons', i)] = dsttemplate.format(number)


# Building
def get_directory_size(directory, exclude=[]):
    result = os.path.getsize(directory)
    for i in os.listdir(directory):
        if i in exclude:
            continue
        i = join(directory, i)
        if os.path.isfile(i):
            result += os.path.getsize(i)
        elif os.path.isdir(i):
            result += get_directory_size(i)
    return result

os.makedirs('build/DEBIAN')

with open('build/DEBIAN/md5sums', 'w') as md5sums:
    for src, dst in FILES.items():
        os.makedirs(dirname(join('build', dst)), exist_ok=True)
        with open(src, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        print(md5, dst, sep='  ', file=md5sums)
        dst = join('build', dst)
        shutil.copy(src, dst)
        subprocess.call(['chmod', '644', dst])
subprocess.call(['chmod', '755', 'build/usr/bin/the-simple-noteprogram'])

with open('build/DEBIAN/control', 'w') as control:
    control.write("""\
Package: the-simple-noteprogram
Priority: optional
Section: x11
Installed-Size: {size}
Maintainer: {maintainer}
Architecture: all
Version: {version}
Depends: python3-appdirs, python3-psutil, python3-gi, gir1.2-gtk-3.0,\
 gir1.2-gtk-3.0, gir1.2-appindicator3-0.1
Description: {short_desc}
{long_desc}
""".format(
        size=math.ceil(get_directory_size('build', exclude=['DEBIAN']) / 1024),
        maintainer=about.AUTHORS[0],
        version=about.VERSION,
        short_desc=about.SHORT_DESCRIPTION,
        long_desc=textwrap.indent(textwrap.fill(about.LONG_DESCRIPTION, 71), ' '),
    ))

subprocess.call(['dpkg-deb', '--build', 'build',
                 'the-simple-noteprogram.deb'])
