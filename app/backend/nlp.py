import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
n4 = stopwords.words('spanish')


def _function_nlp_(papers, steamming=False, stopword = True):
    for x,p in enumerate(papers):        
        p = p.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        p = re.sub('[^A-Za-z0-9ñ]+',' ',p)
        papers[x] = p.split()
        if stopword:
            papers[x] = _function_stopwords_(papers[x])
        if steamming:
            papers[x] = _function_steamming_(papers[x])
    return papers

def _function_stopwords_(paper):
    paper_copy = paper[:]
    for i in paper:
        if i in n4:
            paper_copy.remove(i)
    return paper_copy

def _function_steamming_(paper):
    stemmer = PorterStemmer()
    word=[]
    for i in paper:
        word.append(stemmer.stem(i))
    return word

""" Funcion para steaming para palabras permitidas"""
def _steaming_words_permit(words):
    words = _function_nlp_(words,stopword=False)
    list = []
    for w in words:
        list.append(' '.join(w))
    return list
