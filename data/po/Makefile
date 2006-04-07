# gpodder translation makefile

default:
	for langfile in *.po; do echo -n $${langfile}; msgmerge -U $${langfile} ../messages.pot; mkdir -p ../locale/`basename $${langfile} .po`/LC_MESSAGES/; msgfmt $${langfile} -o ../locale/`basename $${langfile} .po`/LC_MESSAGES/gpodder.mo; done

clean:
	rm -rf ../locale *~ *.mo

.PHONY: default clean
