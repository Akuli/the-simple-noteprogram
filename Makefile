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

PREFIX=$(shell cat prefix-selection 2> /dev/null || echo /usr/local)


all:
	@echo "You can use these commands:"
	@echo "     make run            run without installing"
	@echo "     make install        install to $(PREFIX)"
	@echo "     make uninstall      uninstall from $(PREFIX)"
	@echo "     make select-prefix  select a custom install location"

# TODO: add a 'deb' rule for making Debian packages

clean:
	rm -rf prefix/lib/the-simple-noteprogram/the_simple_noteprogram/__pycache__
	rm -rf build
	rm -f prefix-selection
	rm -f messages.pot

fix-perms:
	chmod 755 build-scripts/select-prefix
	chmod 755 prefix/bin/the-simple-noteprogram

# This option uses pygettext to make a messages.pot
get-pot:
	pygettext prefix/lib/the-simple-noteprogram/the_simple_noteprogram/*.py

install:
	make clean
	cd prefix; find -type d -exec mkdir -p --mode=755 $(PREFIX)/{}    \;
	cd prefix; find -type f -exec install  --mode=644 {} $(PREFIX)/{} \;
	chmod 755 $(PREFIX)/bin/the-simple-noteprogram
	make update-caches

run:
	make fix-perms
	prefix/bin/the-simple-noteprogram

select-prefix:
	chmod 755 build-scripts/select-prefix
	build-scripts/select-prefix

uninstall:
	make clean
	cd prefix; find -type f -exec rm    $(PREFIX)/{} 2> /dev/null \;
	cd prefix; find -type d -exec rmdir $(PREFIX)/{} 2> /dev/null \;
	make update-caches

update-caches:
	xdg-icon-resource forceupdate
	xdg-desktop-menu forceupdate
