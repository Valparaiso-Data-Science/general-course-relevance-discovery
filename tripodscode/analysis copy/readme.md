# Analysis
The analysis folder houses all the code responsible for parsing through the catalog csv outputted from the source directory. 

## Running the code

In order to run this stage of the pipeline, run

```
python3 main.py
```
## How it works

main.py takes in the csv in the courses directory and the terms inputted by the user and feeds them into the recommend_courses function called from course_recs.py. The output from this function is saved as test_save_course_recs.csv using the save_course_recs function from course_recs.py as well.

### Options for analysis

The switch from the analysis of courseID to Description and vice versa can be made by editing line 70 in the recommend_courses function in course_recs.py to "courseID" or "Descriptions".
