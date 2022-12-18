# Source

This directory houses the code responsible for parsing through the course catalog XML and converting it into a csv. This is the csv that will be sent to the analysis folder for further analysis.

## Running the code

In order to run this stage of the pipeline, run

```
python3 main.py
```

## How it works

main.py first calls prep.prepare from prep.py. This function creates the temporary directory to house the trimmed XML, and clears/creates the courses directory where the catalog csv will go. Next, main.py calls createDATA.createCSV() from createDATA.py which takes the catalog XML in the XMLs directory and converts it into a csv. This csv is then stored in the courses directory for further analysis.
