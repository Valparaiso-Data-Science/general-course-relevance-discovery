.POSIX:

all:



setup:
	python3 devel/grobid/getgrobidpythonclient.py ./devel/grobid/
	python3 devel/getReqs.py
	@echo "-----\nIf you are wanting to run grobid, you will need to run: 'python3 devel/grobid/getgrobid.py'\n-----"

csv:
	python3 source/createDATA.py source/
	@echo "Valpo is not included in the output CSV"

stratKfold:
	python3 source/ML.py source/ courses/AllSchools.csv stratKfold

svm:
	python3 source/ML.py source/ courses/AllSchools.csv svm

randForest:
	python3 source/ML.py source/ courses/AllSchools.csv randForest

clean:
	rm -rf courses/
	rm -rf temp_data/

.PHONY: csv clean setup
