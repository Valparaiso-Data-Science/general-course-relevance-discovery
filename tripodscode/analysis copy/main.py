import course_recs

school_df = course_recs.import_df("../courses/parsedcatalog.csv")
clean_terms = course_recs.load_terms("../../search_terms.txt")
output_df = course_recs.recommend_courses(clean_terms, school_df)
course_recs.save_course_recs("./final_results", "test_save_course_recs.csv", output_df)


