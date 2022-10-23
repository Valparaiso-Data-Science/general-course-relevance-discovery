from locale import D_FMT
import pytest
import numpy as np
import pandas as pd
from course_recs import *


def test_import_df():
    df = pd.DataFrame(
    {
        "School": ["SmithSUPERTRIMMED","SmithSUPERTRIMMED","SmithSUPERTRIMMED","SmithSUPERTRIMMED"],
        "CourseID": ["CLT 100 Introduction to Comparative Literature: The Pleasures of Reading", "FRN 262 After Algeria: Revolution Republic and Race in Modern France", "FYS 165 Childhood in African Literature", "AFR 218 History of Southern Africa (1600 to about 1900)"],
        "Descriptions": ["Topics May be repeated once with a different", "From the colonial", "A study of childhood as an", "The history of Southern Africa which"]
    },
    columns=["School", "CourseID", "Descriptions"],
    )
    
    expected = df

    assert import_df("Smith-07-10-2020-FROZEN.csv").to_dict() == expected.to_dict()

def test_load_terms():
    expected = ["collaborative system", "accuracy metrics", "agile data driven", "artificial intelligence", "cloud computing", "big data infrastructures", "bpm", "business analytics", "business intelligence", "cloud powered services", "cognitive technologies", "continuous improvement cycle", "crp", "customer relations management", "data access","data analysis applications", "data analytics"]
    assert load_terms("test_bok.txt").sort() == expected.sort()

#recommend_courses
def test_recommend_courses():
    test_course_df = pd.DataFrame(
        {
            "School": ["SmithSUPERTRIMMED"],
            "CourseID": ["AFR 218 History of Southern Africa (1600 to about 1900)"],
            "Descriptions": ["The history of Southern Africa which"],
            "FoundTerms": ['africa']
           
        },
        columns=["School", "CourseID", "Descriptions", "FoundTerms"],
    )
    expected = test_course_df
    test_clean_terms = ['canada', 'africa']
    assert recommend_courses(test_clean_terms, import_df("Smith-07-10-2020-FROZEN.csv")).to_dict() == expected.to_dict()


def test_save_course_recs():
    expected = "test_save_course_recs.csv"
    test_dir_name = "./tests"
    test_out_filename = "test_save_course_recs.csv"
    test_course_dataframe = pd.DataFrame(
        {
            "School": ["SmithSUPERTRIMMED"],
            "CourseID": ["AFR 218 History of Southern Africa (1600 to about 1900)"],
            "Descriptions": ["The history of Southern Africa which"],
            "FoundTerms": ['africa']
           
        },
        columns=["School", "CourseID", "Descriptions", "FoundTerms"],
    )

    assert save_course_recs(test_dir_name, test_out_filename, test_course_dataframe) == expected