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

fix-perms:
	chmod 755 build-scripts/select-prefix
	chmod 755 prefix/bin/the-simple-noteprogram

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
