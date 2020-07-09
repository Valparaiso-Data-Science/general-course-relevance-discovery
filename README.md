# general-course-relevance-discovery

This repo is intended to house code that allows for data science topics discovery from university course catalogs

## Getting Started

### With Docker (Recommended)

This is the recommended route to take, because all of the dependencies are in the image.

Go into the devel/docker folder and look at the readme and follow the steps there.

### On your personal computer

Make sure that you have python 3 installed, a version of make, and optionally a POSIX compliant shell interpreter (bash or dash will work).
To install all of the required dependencies, run:
```
make setup
```

You will also need the 'enchant' c library installed:
* Linux/BSD users - just use your package manager
* macOS users - getReqs.py takes care of it for you, just make sure you have homebrew installed
* Windows users - you're on your own

### Creating the Dataset

If you want to just create the dataset, its as easy as running:
```
make csv
```
This will create 'AllSchools.csv' under courses, and with our current data, should get you around 60 thousand courses.

## Repo Structure

This repo has a number of direcories, each with a function.
* *pre/* - Has shell script that are made for preprocessing XML files
* *source/* - Has all of the python code that does all of the 'magic'
* *source/tests/* - Contains all of the pytest tests for the repo
* *courses/* - The output csvs that we run machine learning on
* *fullPDFs/* - The source XML (aka the raw data)
* *devel/* - Contains things related to development and running the code.
* *devel/grobid* - Contains scripts that can get grobid set up

## Important Files

* Makefile - The makefile that allows for parts of the code to be done in 'stages'
* bok.txt - Edison body of knowledge words that are agreed to describe data science
* Catalogs.csv - csv file that has line numbers where courses begin and end (for use with fileTrimmer.sh)
* devel/known\_bugs - Known bugs are kept here, instead of ussing issues
* requirements.txt - Contains all of the python libraries that are needed for this project (generated via 'pipreqs --force' in the project /)
* devel/todo - current todo list for the project
* devel/docker/Dockerimage - the docker image for this project
* devel/grobid/urls.csv - csv file that has all of the urls for different pdfs

## Development Guidelines

* Small commits (easily understood)
* Branches for new features (as to not disrupt people using master)

Current Branches:
* master
* machine-learning
* sasha

Historical Branches: (in order of most recent)
* grobid_testing
* syd-test-analysis
* tfix
* superninja
* docker
* nfrankie
* wordninja
* frankie
* unit-tests
* pdf\_layout\_analysis
* refactored-code
* proto
