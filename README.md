# general-course-relevance-discovery
This repo is intended to house code that allows for data science topics discovery from university course catalogs

Pdf.py TODO list
  Need to get rid of newlinds in 'updated' array of lines because part of our regex includes checking the next line for a capital letter (Cody can explain) but if their is a space between we would have to if statement account for it, id rather not have to worry about spacings. I previously used filter() but I coulded range(len()) a filter object so if you can revert it back that would work nicely

  Need to find an end case, not all courses end at the last page, we need to think of a way to differentiate courses from classes. Some split between fields/majors and then the last major ends but the catalog keeps rambling

  Output to a file other than our current write to text

  Either in Py or in the "CSV naive regex" we need to merge duplicate classes found (I think this will be easier in the CSV cleaning rather than the py stuff, py is getting kinda complex)

  Another way to refine the regex is we already check 1st line for MATH 220, we check the 2nd line (which is the 3rd line cause formatting issues rn) for a capital letter (the start of a title always capital)
  BUT now we can add a search to the 3rd line (which idk if its the 4th or 5th cause of newlines but we need to clear that too) for a capital A and space or a capital letter and lowercase letter (courses start with"A study about..." or "The study of")