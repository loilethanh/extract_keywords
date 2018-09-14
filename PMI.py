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
from collections import Counter


def pmi_1word(count ,term):
    return ( - math.log(count[term]))


def pmi_2word(count ,term1, term2):
    return math.log(pmi_numerator(count, term1, term2 )/pmi_denominator(count,term1,term2))


def pmi_3word(count ,terms):
    pmi_12 = pmi_2word(count , terms[0],terms[1])
    temp_term = terms[1] +" "+ terms[3]
    pmi_23 = pmi_2word(count, terms[0],temp_term)
    return (pmi_23 - pmi_12)


def pmi_denominator(count, term1, term2):
    fre_term1 = count[term1]
    fre_term2 = count[term2]
    return ( 1.0 * fre_term1 * fre_term2)


def pmi_numerator(count , term1, term2):
    string = term1 + " " + term2
    fre_term = count[string]
    N = len(count)
    return (1.0 * N * fre_term)


if __name__ == '__main__':
    # str = "viet nam 2018 khac viet nam nam 2010"
    # data = word_grams(str.split(" "))
    # wordcount = Counter(data)
    # print(len(wordcount))
    # with open("count.pkl",'wb') as file :
    #     pickle.dump(wordcount,file)

    with open("count.pkl",'rb') as file :
        abc = pickle.load(file)

    print(pmi_1word(abc,"viet"))





