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
    doc_set = getData()
    stop_words = load_stopwords_tfidf(stoppath)
    build_models(doc_set,file_model,True)
