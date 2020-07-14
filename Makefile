.POSIX:

all:



setup:
	python3 devel/grobid/getgrobidpythonclient.py ./devel/grobid/
	python3 devel/getReqs.py
	@echo "-----\nIf you are wanting to run grobid, you will need to run: 'python3 devel/grobid/getgrobid.py'\n-----"

csv:
	python3 source/createDATA.py source/
	sh pre/parsevalpo.sh fullPDFs/ucat1920.xml courses/
	mv courses/AllSchools.csv courses/all.csv
	cat courses/all.csv courses/valpo.csv > courses/AllSchools.csv
	rm courses/all.csv

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: csv clean setup
