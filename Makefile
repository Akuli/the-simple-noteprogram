# Edit this line to install to a custom location
PREFIX=/usr/local


VERSION=$(shell cd prefix/lib/the-simple-noteprogram; python3 -c 'from the_simple_noteprogram import about; print(about.VERSION)')
SHORTDESC=$(shell cd prefix/lib/the-simple-noteprogram; python3 -c 'from the_simple_noteprogram import about; print(about.SHORT_DESCRIPTION)')
LONGDESC=$(shell cd prefix/lib/the-simple-noteprogram; python3 -c 'from the_simple_noteprogram import about; print(about.LONG_DESCRIPTION)' | fold -w 71 -s | while read i; do echo " $i"; done)


all:
	@echo "Run 'make install' to install The Simple Noteprogram $(VERSION)"
	@echo "to $(PREFIX) or 'make uninstall' to uninstall it from there."

install:
	make clean
	cd prefix; find -type d -exec mkdir -p --mode=755 $(PREFIX)/{} \;
	cd prefix; find -type f -exec install --mode=644 {} $(PREFIX)/{} \;
	chmod 755 $(PREFIX)/bin/the-simple-noteprogram
	make update-caches

uninstall:
	cd prefix; find -type f -exec rm $(PREFIX)/{} \;
	cd prefix; find -type d -exec rmdir $(PREFIX)/{} 2> /dev/null \;
	make update-caches

update-caches:
	xdg-icon-resource forceupdate
	xdg-desktop-menu forceupdate

deb:
	make clean
#	cp -r prefix build
	echo $(VERSION)

clean:
	rm -rf prefix/lib/the-simple-noteprogram/the_simple_noteprogram/__pycache__
	rm -rf build
