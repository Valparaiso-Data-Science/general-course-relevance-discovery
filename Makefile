.POSIX:

all:



setup:
	python3 devel/grobid/getgrobidpythonclient.py
	python3 devel/getReqs.py

db:
	python3 source/main.py

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: db clean
