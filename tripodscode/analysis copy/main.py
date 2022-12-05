import course_recs
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib

school_df = course_recs.import_df("../courses/parsedcatalog.csv")
clean_terms = course_recs.load_terms("../../search_terms.txt")
output_df = course_recs.recommend_courses(clean_terms, school_df)
course_recs.save_course_recs("./final_results", "test_save_course_recs.csv", output_df)

course_recs.resultsLoaded()
# def sendResponse(email):
#     message = MIMEMultipart()
#     message["from"] = "Tripods"
#     message["to"] = str(email)
#     message["subject"] = "This is the response"
#     message.attach(MIMEText("Here are your results"))

#     with smtplib.SMTP(host="cnguyen49@smith.edu", port=587) as smtp:
#         smtp.ehlo()
#         smtp.login("user", "pass")
#         smtp.sendmail(send_from, send_to, msg.as_string())
#         smtp.close()

