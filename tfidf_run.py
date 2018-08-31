import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim import  corpora
from nltk.util import ngrams
from src.tfidf import *
from setup import *
from src.tfidf_v2 import *
import datetime
from datetime import timedelta
from src.auto_gettag import *
from src.auto_gettag import *


# #
if __name__ == '__main__':
#
    # date_ = get_lastday_file(file_update)
    doc_set = getData()
    last_Date = doc_set[len(doc_set) - 1]['insertDate']
    print(len(doc_set), "  ", last_Date)
#     # write_file_(last_Date)
#     stop_words = load_stopwords_tfidf(stoppath)
#     # dictionary,models = build_dict(doc_set,stop_words)
#
#     # dictionary_, model_ = update_dict(doc_set, dictionary, stop_words)
#     # start = time.time()
#     # results = get_tfidf(stop_words, doc_set[0], model_, dictionary_)
#
#     time.clock()
#     while True:
#         # dictionarys = Dictionary.load(dictionary_file)
#         # models = TfidfModel.load(model_tfidf_file)
#         # print(len(dictionarys),dictionarys)
#         # date = get_lastday_update()
#         doc_set = getData()
#         # last_Date = doc_set[len(doc_set) - 1]['insertDate']
#         # print(len(doc_set), "  ", last_Date)
#         # write_file_(last_Date)
#         print(len(doc_set))
#         update_models = True
#         print(update_models)
#
#         update_models = False
#         print(update_models)
#
#         # update_dict(doc_set, dicti, stop_words)
#         # start = time.time()
#     #     results = get_tfidf(stop_words,doc_set[0], models,dict)
#     #     # print("time to get : ",time.time() - start)
#     #     # print(results)
#         time.sleep(1)
#         print("========================end=========================")