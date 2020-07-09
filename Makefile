.POSIX:

all:



setup:
	python3 devel/grobid/getgrobidpythonclient.py ./devel/grobid/
	python3 devel/getReqs.py
	echo "-----\nIf you are wanting to run grobid, you will need to run: 'python3 devel/grobid/getgrobid.py'\n-----"

csv:
	python3 source/CreateCSV.py

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: db clean setup
