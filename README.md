# general-course-relevance-discovery

This repo is intended to house code that allows for data science topics discovery from university course catalogs

## Getting Started
Make sure that you have python 3 installed and optionally a POSIX compliant shell interpreter (bash or dash will work).
To install all of the required dependencies, run:
```
python getReqs.py
```

You will also need the 'enchant' c library installed:
* Linux and BSD users - just use your package manager
* macOS users - getReqs.py takes care of it for you, just make sure you have homebrew installed
* Windows users - you're on your own

## Repo Structure

This repo has a number of direcories, each with a function.
* *pre/* - Has shell script that are made for preprocessing XML files
* *source/* - Has all of the python code that does all of the 'magic'
* *source/tests/* - Contains all of the pytest tests for the repo
* *courses/* - The output csvs that we run machine learning on
* *fullPDFs/* - The source XML (aka the raw data)

## Important Files

* bok.txt - Edison body of knowledge words that are agreed to describe data science
* known\_bugs - Known bugs are kept here, instead of ussing issues
* requirements.txt - Contains all of the python libraries that are needed for this project

## Development Guidelines

* Small commits (easily understood)
* Branches for new features (as to not disrupt people using master)
