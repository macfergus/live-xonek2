#!/bin/sh

if [ ! -f .livedir ] ; then
	find {~,/Applications} -path \*Live\* -name MIDI\ Remote\ Scripts | head -1 > .livedir
fi
cat .livedir
