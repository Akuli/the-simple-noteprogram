# This file is for GNU operating systems, such as most Linux
# distributions.

# Edit to install to a custom location, if you install to a non-standard
# prefix you may need to edit some files to get all features to work
PREFIX = /usr/local



ICON_SIZES = 16 22 24 32 48 64 128 256

all:
	@echo "Run 'sudo make install' to install to $(PREFIX) or edit"
	@echo "Makefile and run 'make install' or 'sudo make install' to"
	@echo "install to some other location."

install:
	# Cleaning
	rm -rf src/the_simple_noteprogram/__pycache__
	@echo

	# Copying files
	mkdir -p $(PREFIX)/bin $(PREFIX)/lib
	cp -rT src $(PREFIX)/lib/the-simple-noteprogram
	mv $(PREFIX)/lib/the-simple-noteprogram/data/gnu-linux-launcher $(PREFIX)/bin/the-simple-noteprogram
	chmod a+x $(PREFIX)/bin/the-simple-noteprogram  # just to make sure it's executable
	@echo

	# Installing icons
	$(foreach i, $(ICON_SIZES), xdg-icon-resource install --size $(i) $(PREFIX)/lib/the-simple-noteprogram/icons/the-simple-noteprogram-$(i).png the-simple-noteprogram;)
	@echo

	# Installing the menu entry
	xdg-desktop-menu install $(PREFIX)/lib/the-simple-noteprogram/data/the-simple-noteprogram.desktop
	@echo

uninstall:
	# Uninstalling the menu entry
	xdg-desktop-menu uninstall $(PREFIX)/lib/the_simple_noteprogram/the-simple-noteprogram.desktop
	@echo

	# Uninstalling icons
	$(foreach i, $(ICON_SIZES), xdg-icon-resource uninstall --size $(i) the-simple-noteprogram;)
	@echo

	# Removing files
	rm $(PREFIX)/bin/the-simple-noteprogram
	rm -r $(PREFIX)/lib/the-simple-noteprogram
	@echo

clean:
	# Cleaning
	rm -rf src/the_simple_noteprogram/__pycache__
	@echo

