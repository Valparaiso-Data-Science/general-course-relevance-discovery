.POSIX:

all:



db:
	python3 source/main.py

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: db clean
