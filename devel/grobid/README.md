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

If you've done all of that, you may be ready to take on the beast, type:
```
bash createXMLgrobid.sh
```
or Alternatively:
```
./createXMLgrobid.sh
```

## known issues

There is an issue with pdf size and this method of creating XML files, the error that they throw from GROBID is a 500 error.
For example, the catalog we get from Purdue is just far too big for GROBID to handle and it just spits out a 500 error.

There are two ways at the time of writing we can solve this problem.
1. We can just use Adobe for the offending pdfs.
2. We can split up the pdfs to be smaller.

Since number 1 is pretty straight forward, I think it'd be worthwhile to investigate number 2.

[qpdf](http://qpdf.sourceforge.net/) is a program that can automate the process of splitting PDFs into sections that only contain certain pages.

The manual has this example command to only get even pages between 2 and 20:
```
qpdf --pages <source>.pdf 1-20:even -- <output>.pdf
```
And to get odd pages from the whole document:
```
qpdf --pages <source>.pdf 1-z:odd -- <output>.pdf
```

If you want to read more on what qpdf can do, the manual is [here](http://qpdf.sourceforge.net/files/qpdf-manual.html).

