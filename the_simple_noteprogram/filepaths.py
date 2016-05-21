"""The filepaths"""
from os.path import abspath, dirname, join
import appdirs

configdir = appdirs.user_config_dir('the-simple-noteprogram')
install_prefix = dirname(dirname(dirname(dirname(abspath(__file__)))))
libdir = join(install_prefix, 'lib')
sharedir = join(install_prefix, 'share')
