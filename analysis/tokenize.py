"""##Word Tokenizer
IN:
- col: column of responses

OUT:
- list_of_lists: list of lists tokenized by word without any preprocessing
"""

def tokenize(col):
    #creates list of lists, inside lists contains sentences tokenized by word
    list_of_lists = []
    for sentence in col:
      tokens = nltk.word_tokenize(str(sentence))
      list_of_lists.append(tokens)
    return list_of_lists
