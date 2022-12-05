# general-course-relevance-discovery

This repo is intended to house code that allows for data science topics discovery from university course catalogs

## Getting Started

### With Anaconda (Recommended)

Go to anaconda.com and install Anaconda.

### On your personal computer

To create a conda environment with all of the requirements, cd into the directory with the tripods.yml file (general-course-relevance-discovery), open your terminal environment and run
```
conda env create --file tripods.yml   
```
Now you should have an environment with all the requirements installed.

In order to use the environment, run

```
conda activate tripods
```
To deactivate the environment run

```
conda deactivate
```
### Creating the Dataset

If you want to just create the dataset, it's as easy as running:
```
make csv
```
This will create 'AllSchools.csv' under courses, and with our current data, should get you around 60 thousand courses.

### Machine Learning

Currently the machine learning code is not finished yet, however you can make the test train split for the machine learning.

To make the test-train split, run:
```
make stratKfold
```

To run the other machine learning code (which is still experimental at this stage), run:
```
make randForest
```
Or:
```
make svm
```

To run the code associated with Random Forest, or the Support Vector Machine respectively.

It is also important to note that both `randForest` and the `svm` do not work at the time of
writing (7-17-2020). If you run the above commands, you are not going to get any meaningful
output.

## Repo Structure

This repo has a number of directories, each with a function.
* *pre/* - Has shell scripts that are made for preprocessing XML files
* *source/* - Has all of our python code that does all of the proverbial 'magic'
* *source/tests/* - Contains all of the pytest tests for the repo
* *courses/* - The output csvs that we run machine learning on
* *fullPDFs/* - The source XML (aka the raw data)
* *devel/* - Contains things related to development and running the code.
* *devel/docker/* - Contains the Dockerfile
* *devel/grobid/* - Contains scripts that can get grobid set up

## Important Files

* Makefile - allows for parts of the code to be done in 'stages' (abstraction)
* bok.txt - Edison body of knowledge words that are agreed to describe data science
* Catalogs.csv - csv file that has line numbers where courses begin and end
* devel/known\_bugs - Known bugs are kept here, instead of ussing issues
	* Not used anymore
* requirements.txt - Contains all of the python libraries that are needed for this project (generated via 'pipreqs --force' in the project /)
* devel/todo - current todo list for the project
	* Not used anymore
* devel/docker/Dockerimage - the docker image for this project
* devel/grobid/urls.csv - csv file that has all of the urls for different pdfs
* devel/grobid/createXMLgrobid.sh - shell script that automates the process of converting pdfs with grobid

## GROBID

We are in the process of moving to grobid for doing our pdf to xml conversion for college pdfs that support it.

Our current code assumes that you are using Adobe Acrobat for the pdf to XML conversion, and for some catalogs, it is the only way we can convert it (Purdue, MIT, Carnegie Mellon, etc.).

If you want to test our GROBID code, head over to `devel/grobid/` and have a look at the README.

## Development Guidelines

* Small commits (easily understood)
* Branches for new features (as to not disrupt people using master)

Current Branches:
* main

Historical Branches: (in order of most recent)
* machine-learning
* frankie

## License

The code is under the ECL-2.0
