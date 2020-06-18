"""##Process Responses Across All Columns Function
IN:
- stops: list of stop words
- df: dataframe of all courses
No OUT, creates a dictionary of dictionaries containing processed responses sorted by each school for usage in TF IDF analysis
"""

def process_words(stops,df):
  og_dict = {} #dictionary of full responses
  responses = {} #dictionary of processed responses
  school = df['School'][0]
  og_dict[school] = []
  i=0
  for s in df['School']:
    if s == school:
      r = df['Descriptions'][i] #description string
      og_dict[school].append(r)
      i+=1
    else:
      school = s
      og_dict[school] = []
      r = df['Descriptions'][i] #description string
      og_dict[school].append(r)
      i+=1

  for s in list(og_dict.keys()):
    temp_list = tokenize(og_dict[s])
    responses[s] = []
    for lst in temp_list:
      lst = ' '.join(lst)
      wr_string = lst.lower()
      doc = nlp(wr_string)
      new_sent = " ".join([token.lemma_ for token in doc])
      new_sent = new_sent.split()
      new_sent = [word for word in new_sent if word not in stops]
      new_sent = ' '.join(new_sent) #completely processed sentence as string
      responses[s].append(new_sent)
  return responses, list(og_dict.keys()) #returns processeed response dictionary & school names