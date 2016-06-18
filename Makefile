REMOTEDIR:=$(shell ./find_live_remote_dir.sh)
DESTDIR=$(REMOTEDIR)/XoneK2

.PHONY: install
install:
	mkdir -p '$(DESTDIR)'
	rm -f '$(DESTDIR)'/*.pyc
	install XoneK2/__init__.py '$(DESTDIR)'
	install XoneK2/xone.py '$(DESTDIR)'
