.POSIX:

all:



db:
	python3 source/CreateDB.py

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: db clean
