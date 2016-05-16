"""The filepaths"""
from os.path import abspath, dirname, join
import appdirs
from . import about

configdir = appdirs.user_config_dir(about.DASHES)
install_prefix = dirname(dirname(dirname(dirname(abspath(__file__)))))
libdir = join(install_prefix, 'lib')
sharedir = join(install_prefix, 'share')
