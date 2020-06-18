"""##TF-IDF Function
IN:
- dictionary: dictionary being accessed
- schools: list of school names

No OUT, creates csv file for each category in categories
"""

def tfidf(dictionary, schools):
  nlp = spacy.load("en")
  answers = dictionary
  corpus = []
  #for school in schools:
    #doc_string = ' '.join(dictionary[school])
    #corpus.append(doc_string)
  for school in schools:
    print("School: %s -----------------" % school)
    corpus=dictionary[school]
    #code from https://www.geeksforgeeks.org/tf-idf-for-bigrams-trigrams/
    #GETTING BIGRAMS
    vectorizer = CountVectorizer(ngram_range = (1,1)) 
    X1 = vectorizer.fit_transform(corpus)  
    features = (vectorizer.get_feature_names()) 
   
    # Applying TFIDF 
    vectorizer = TfidfVectorizer() 
    vectors = vectorizer.fit_transform(corpus) 
    scores = (vectors.toarray()) 
    # Getting top ranking features 
    sums = vectors.sum(axis = 0) 
    data1 = [] 
    for col, term in enumerate(features): 
        data1.append( (term, sums[0,col] )) 
    ranking = pd.DataFrame(data1, columns = ['term','rank']) 
    words = (ranking.sort_values('rank', ascending = False)) 
    words = words[:10]

    #Getting frequency counts
    freq_list = []
    list_bigram = list(words['term'])
    i = 0
    while i < 10:
      bigram = str(list_bigram[i]).split()
      f_word = str(bigram[0])
      #s_word = str(bigram[1])
      regex = re.escape(f_word) #+ r" " + re.escape(s_word)
      count = 0 
      for doc in corpus:
        iterator = finditer(regex, doc)
        for match in iterator:
          count+=1
      app = str(count)
      freq_list.append(app)
      i+=1
    words['frequency'] = freq_list
    denom = len(dictionary[school])
    words ['overall'] = str(denom)
    words['category'] = school
    words = words[['category','term','frequency','overall','rank']]
    print('\n',words)
    print("\n---------------------------\n")
'''
    #saving dataframe to csv
    path_name = 'TFIDF_' + school +'.csv'
    words.to_csv(path_name)
'''
