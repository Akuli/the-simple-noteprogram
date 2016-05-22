"""The filepaths"""
import os
from os.path import abspath, dirname, join
import appdirs

_prefix = dirname(dirname(abspath(__file__)))
datadir = join(_prefix, 'data')
icondir = join(_prefix, 'icons')
localedir = join(_prefix, 'locale')

configdir = appdirs.user_config_dir('the-simple-noteprogram')
os.makedirs(configdir, exist_ok=True)
