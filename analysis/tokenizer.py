
import nltk
import spacy
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize

def tokenize(col):
    #creates list of lists, inside lists contains sentences tokenized by word
    list_of_lists = []
    for sentence in col:
      tokens = nltk.word_tokenize(str(sentence))
      list_of_lists.append(tokens)
    return list_of_lists
