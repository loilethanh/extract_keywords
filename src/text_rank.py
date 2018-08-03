import csv
from summa import keywords
import gensim
from nltk.corpus import stopwords
from summa.summarizer import summarize
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA
start = 0
limit = 2

# file = open('result/textrank.txt', 'w')
# file_sum = open('summarys.txt', 'w')
file_path = "data/data_news_soha.csv"


def getData():
    data = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id':row['newsId']}
            content = row['title_token'].lower() +" "+ row['sapo_token'].lower()+ " " + row['content_token'].lower()
            dict_content = {"content" : content}
            dict.update(dict_content)
            data.append(dict)
    return data[start:limit]


def load_postag ():
    data_postag = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in  reader :
            content = ''
            id = row['newsId']
            content +=row['title_postag']+" "+row['sapo_postag']+" "+row['content_postag']
            content_postag ={}
            word_tokens = word_tokenize(content)
            for word in word_tokens :
                w = ''
                postag = ''
                for i in range(len(word)):
                    if word[i] == "/" :
                        w = word[:i].lower()
                        postag = word[i+1:]
                        break
                content_postag.update({w:postag})
            data_postag.append({'id':id,'content_postag':content_postag})
    return data_postag

def loadStopwords():
    data_pos = load_postag()
    # pos = ['A','B','C','Cc','I','T','X','Z','R','M','CH','E','L','p']
    pos = ['C', 'Cc', 'M', 'A', 'E', 'M', 'R', 'T', 'X']
    stop_words = []
    for x in open('data/stoplists/vietnamese-stopwords.txt', 'r').read().split('\n'):
        d = ''
        w = x.split(" ")
        if len(w)== 1 :
            stop_words.append(w[0])
        else :
            for i in range(len(w)-1) :
                d+=w[i]+"_"
            d+=w[len(w)-1]
            stop_words.append(d)

    for d in data_pos :
        for w in d['content_postag'] :
            if(d['content_postag'][w] in pos ) :
                stop_words.append(w)
    return stop_words



def textRank(data) :
    stopwords = loadStopwords()
    keywords_textrank = []
    for d in data:
        content = d['content']
        word_tokens = word_tokenize(content)
        filter_sentence = ''
        for w in word_tokens:
            wo = w.lower()
            if not wo in stopwords:
                filter_sentence += wo + " "
        key = keywords.keywords(filter_sentence ,scores=False ).split("\n")
        # file.write(str(d['id'])+" "+str(key))
        print(d['id'], key ,"\n")
        keywords_textrank.append({'id':d['id'],'keywords':key})
    return keywords_textrank



def summary(data) :
    summarys = []
    for d in data :
        summarys.append(summarize(d['content'],ratio= 0.2 ))
        print(summarize(d['content'],ratio= 0.2 ))
        # file_sum.write(str(d['id'])+"  "+ summarize(d['content'],language='vietnam', ratio= 0.2 )+"\n")

def gensim_texrank(data) :
    stopwords = loadStopwords()
    keywords_textrank = []
    for d in data:
        content = d['content']
        word_tokens = word_tokenize(content)
        filter_sentence = ''
        for w in word_tokens:
                if not w in stopwords:
                    filter_sentence += w + " "
        kw = gensim.summarization.keywords(filter_sentence,ratio=0.2,words=None,scores=True,deacc=True)
        print(d['id'],kw)


if __name__ == '__main__' :
    data = getData()
    # gensim_texrank(data)
    text_ranks = textRank(data)













