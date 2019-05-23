# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:30:05 2019

@author: nrandle
"""


classes = {"CLS 217":"Greek Art and Archaeology Same as ARH 217. This course is a contextual examination of the art and architecture of Ancient Greece, from the end of the Bronze Age through the domination of Greece by Rome (ca. 1100-168 BCE) and handles an array of settlements, cemeteries, and ritual sites. It tracks the development of the Greek city-state and the increasing power of the Greeks in the Mediterranean, culminating in the major diaspora of Greek culture accompanying the campaigns of Alexander the Great and his followers. The course takes a broadly chronological approach, and the question of a unified Greek culture is stressed. Continuing archaeological work is considered. (E){A} {H} Credits: 4 Rebecca Worsham Normally offered in alternate years",
        "CLS 227":"Classical Mythology The principal myths as they appear in Greek and Roman literature, seen against the background of ancient culture and religion. Focus on creation myths, the structure and function of the Olympian pantheon, the Troy cycle and artistic paradigms of the hero. Some attention to modern retellings and artistic representations of ancient myths. {A} {L} Credits: 4 Members of the department Normally offered in alternate years",
        "DATA 151":"Introduction to Data Science 2+3, 3 Cr. Introduction to the use of computer based tools for the analysis of large data sets for the purpose of knowledge discovery. Students will learn to understand the Data Science process and the difference between deductive hypothesis?driven and inductive data?driven modelling. Students will have hands?on experience with appropriate on?line analytical processing and data mining software platforms, and will complete a project using real data. Pre?requisite: MATH 115, or placement higher than MATH 115 in the Math Placement process, or one of STAT 140, STAT 240, IDS 205, or CE 202.",
        "DATA 433":"Data Mining and Applications 2+2, 3 Cr. Data mining is a broad area that integrates techniques from several fields, including machine learning, statistics, pattern recognition, artificial intelligence, and database systems, for the analysis of large volumes of data. This course gives a wide exposition of these techniques and their software tools. Prerequisite: DATA 151 or CS 157 and one of STAT 140, STAT 240, IDS 205, PSY 201, or CE 202. Students may not receive credit for both DATA 433 and BUS 440.",
        "ECON 325":"Econometrics 3 Cr. The application of mathematical and statistical techniques to the analysis of economic issues. Development of simple and multiple regression as tools of analysis. Use of computer facilities and statistical programs to apply the tools to current economic data. Prerequisites: ECON 221, ECON 222, MATH 131 and one of the following: STAT 140, STAT 240, PSY 201, or IDS 205."
        }

def findRelevant(classes):
                    
    bagWords = open("../bok.txt").read().splitlines()
    result = {}
    
    for i,j in classes.items():
        for l in bagWords:
            if l in j:
                result[i] = j
    return result