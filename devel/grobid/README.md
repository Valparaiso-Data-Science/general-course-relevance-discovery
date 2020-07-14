# grobid

This folder is meant to house things that are related to grobid, in an effort to declutter the repository.

## getting grobid

The two scripts in this directory are responsible for gettting grobid, as well as the python client for grobid.

You can execute them like this:
```
python3 getgrobid.py
```
Or Alternatively:
```
./getgrobid.py
```

## getting xmls from grobid

Requirements:
	* The python grobid client (should be downloaded with `make setup`)
	* Grobid running (createXMLgrobid.sh should take care of this for you)
	* Making sure that the year in 'createXMLgrobid.sh' is set to what you want.
		* Options:
			* Numerical year (15-16, 17-18, etc.)
			* 'All' - for every pdf we have in urls.csv
			* 'latest' - for the latest pdf from every school

