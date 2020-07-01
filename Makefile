.POSIX:

all:



setup:
	echo "If you are wanting to run grobid, you will need to run:
		python3 devel/grobid/getgrobid.py"
	python3 devel/grobid/getgrobidpythonclient.py
	python3 devel/getReqs.py

db:
	python3 source/main.py

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: db clean
