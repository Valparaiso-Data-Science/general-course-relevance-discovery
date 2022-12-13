import pytest
import numpy as np
import pandas as pd
from course_recs import *
from sw_scratch import *

def test_check_last_char():
    expected = True
    assert check_last_char("CSC") == expected

def test_check_last_char2():
    expected = False
    assert check_last_char("CSC250") == expected

term_list = ["happy", "sad", "jealous", "bored"]
stopword_list = ["joyful", "ecstatic", "happy"]
def test_terms_remove_stops():
    expected = ["sad", "jealous", "bored"]
    assert terms_remove_stops(term_list, stopword_list).sort() == expected.sort()
#had to sort because .difference was outputting terms out of order

def test_import_df():
    df = pd.DataFrame(
    {
        "School": ["SmithSUPERTRIMMED","SmithSUPERTRIMMED","SmithSUPERTRIMMED","SmithSUPERTRIMMED"],
        "CourseID": ["CLT 100 Introduction to Comparative Literature: The Pleasures of Reading", "FRN 262 After Algeria: Revolution Republic and Race in Modern France", "FYS 165 Childhood in African Literature", "AFR 218 History of Southern Africa (1600 to about 1900)"],
        "Descriptions": ["Topics May be repeated once with a different", "From the colonial", "A study of childhood as an", "The history of Southern Africa which"]
    },
    )
    columns=["School", "CourseID", "Descriptions"],
    expected = df
    print(df)
    print("Actual")
    print(import_df("Smith-07-10-2020-FROZEN.csv"))
    assert import_df("Smith-07-10-2020-FROZEN.csv").to_dict() == expected.to_dict()

def test_load_terms():
    expected = ["collaborative system", "accuracy metrics", "agile data driven", "artificial intelligence", "cloud computing", "big data infrastructures", "bpm", "business analytics", "business intelligence", "cloud powered services", "cognitive technologies", "continuous improvement cycle", "crp", "customer relations management", "data access","data analysis applications", "data analytics"]
    assert load_terms("test_bok.txt").sort() == expected.sort()

# def test_save_course_recs():
#     expected =
#     assert save_course_recs() == expected.sort()