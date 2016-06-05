"""Information about filepaths"""
# If you edit this file make sure it doesn't import anything from
# the_simple_noteprogram. The __init__.py file imports this file and
# sets up internationalization with it, and most other files in
# the_simple_noteprogram need the internationalization.

import os
from os.path import abspath, dirname, isfile, join
import appdirs

user_cache_dir = appdirs.user_cache_dir('the-simple-noteprogram')
user_config_dir = appdirs.user_config_dir('the-simple-noteprogram')
os.makedirs(user_cache_dir, exist_ok=True)
os.makedirs(user_config_dir, exist_ok=True)

prefix = dirname(dirname(dirname(dirname(abspath(__file__)))))

executable = join(prefix, "The Simple Noteprogram.exe")
if not isfile(executable):
    executable = join(prefix, 'bin', 'the-simple-noteprogram')
