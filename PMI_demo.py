import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim import  corpora
from nltk.util import ngrams
from src.tfidf import *
from setup import *
import datetime
from datetime import timedelta
from src.auto_gettag import *
from src.auto_gettag import *
from src.PMI import *


if __name__ == '__main__':

    #
    stop_words = load_stopwords_tfidf(stoppath)
    doc_set = getData()
    print("lenght : ", len(doc_set))

    data = []
    for d in doc_set:
        tokens = tokenizer.tokenize(d['title'] + " " + d['content'])
        stopped_tokens= [word for word in tokens if not word in stop_words]
        ngram = word_grams(stopped_tokens)
        data.append(ngram)


    wordcount  = Counter(data)

    with open(model_pmi, 'wb') as file:
        pickle.dump(wordcount,file)

    with open(model_pmi, 'rb') as file:
        abc = pickle.load(file)

    print(pmi_1word(abc, "viet"))

