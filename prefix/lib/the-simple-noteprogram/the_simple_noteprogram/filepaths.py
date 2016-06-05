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
