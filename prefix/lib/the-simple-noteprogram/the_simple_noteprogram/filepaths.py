"""The filepaths"""
import os
from os.path import abspath, dirname, join
import appdirs

prefix = dirname(dirname(dirname(dirname(abspath(__file__)))))
configdir = appdirs.user_config_dir('the-simple-noteprogram')
os.makedirs(configdir, exist_ok=True)
