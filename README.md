# general-course-relevance-discovery
Repo made to extract data science relevant courses from university course catalogs
See next steps under general-course-relevance-discovery/tripodscode/devel/todo

## Getting Started

### With Anaconda (Recommended)

Go to anaconda.com and install Anaconda.

### On your personal computer
To begin, go to the bottom of the tripods.yml file and change the directory path to match your local device. 

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
## Running TripodsWeb locally

- Begin by downloading Django onto your conda env. https://docs.djangoproject.com/en/4.1/topics/install/ 
- Clone this repository if you have not already. 
- Before running, you will have to customize some code in * general-course-relevance-discovery/courseFinder/views.py*
  - In views.py, change the directory paths to match where you have this repository on your local machine. The lines you will change are 67, 68, 71, 99, 100. 
- Now you are ready to try running the website. In your terminal, go to the directory that holds manage.py
- To run the local server, run this in your terminal:
```
python3 manage.py runserver
```
- This will launch the local server and direct you to a url like "http://127.0.0.1:8000/courseFinder/", the homepage.

- To access the admin page, go to "http://127.0.0.1:8000/admin"
  - Username: tripodsadmin
  - Password: schools
  
- If you change code in models.py, here is how to run the migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
```


## Repo Structure
* *courseFinder/* Holds all the website code.
* *tripodsCode/* This is the new name for the *prexisting general-course-relevance-discovery/* code.
* *tripodsWeb/* This holds the app settings for the website. 
This repo has a number of directories, each with a function.
* Within *tripodsCode/* : 
* *pre/* - Has shell scripts that are made for preprocessing XML files
* *source/* - Has all of our python code that does all of the proverbial 'magic'
* *source/tests/* - Contains all of the pytest tests for the repo
* *courses/* - The output csvs that we run machine learning on
* *XMLs/* - The source XML (aka the raw data)
* *devel/* - Contains things related to development and running the code.
* *devel/docker/* - Contains the Dockerfile
* *devel/grobid/* - Contains scripts that can get grobid set up

## Important Files
* views.py controls the process from submiting a request, to running the XML->CSV->final results->results.html
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

## Development Guidelines

* Small commits (easily understood)
* Branches for new features (as to not disrupt people using master)

## License

The code is under the ECL-2.0


