prefix ?= /usr
bindir ?= $(prefix)/bin
datadir ?= $(prefix)/share
pkgdatadir ?= $(datadir)/hungryipscanner
appdir ?= $(datadir)/applications
icondir ?= $(datadir)/icons/hicolor/scalable/apps

all: hungryipscanner

hungryipscanner:
	echo '#!/bin/sh' > hungryipscanner
	echo 'exec $(prefix)/bin/python3 $(pkgdatadir)/hungryip.py "$$@"' >> hungryipscanner
	chmod +x hungryipscanner

install: hungryipscanner
	install -d $(DESTDIR)$(bindir)
	install -m 0755 hungryipscanner $(DESTDIR)$(bindir)/hungryipscanner

	install -d $(DESTDIR)$(pkgdatadir)
	install -m 0644 hungryip.py $(DESTDIR)$(pkgdatadir)/hungryip.py

	install -d $(DESTDIR)$(appdir)
	install -m 0644 com.github.juliengrdn.hungryipscanner.desktop $(DESTDIR)$(appdir)/com.github.juliengrdn.hungryipscanner.desktop

	install -d $(DESTDIR)$(icondir)
	install -m 0644 hungryipscannerlogo.svg $(DESTDIR)$(icondir)/hungryipscannerlogo.svg

uninstall:
	rm -f $(DESTDIR)$(bindir)/hungryipscanner
	rm -rf $(DESTDIR)$(pkgdatadir)
	rm -f $(DESTDIR)$(appdir)/com.github.juliengrdn.hungryipscanner.desktop
	rm -f $(DESTDIR)$(icondir)/hungryipscannerlogo.svg

clean:
	rm -f hungryipscanner
