from course_recs import *

school_df = import_df("Smith-07-10-2020-FROZEN.csv")
clean_terms = load_terms("sample_bok.txt")
output_df = recommend_courses(clean_terms, school_df)
save_course_recs("./final_results", "test_save_course_recs.csv", output_df)