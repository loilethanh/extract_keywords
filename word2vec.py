from gensim.models import FastText, Word2Vec
import  gensim

from gensim.models import TfidfModel
from gensim import models, corpora
from nltk.tokenize import RegexpTokenizer
import csv, gensim
from nltk.tokenize import word_tokenize
from six import iteritems

from sklearn.feature_extraction.text import TfidfVectorizer

tokenizer = RegexpTokenizer(r'\w+')
file_path = "data/data_news_soha.csv"

start = 0
limit = 1000

def getData():
    data = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content = ''
            dict = {'id': row['newsId']}
            content += row['title_token'] + " " + row['sapo_token'] + " " + row['content_token']
            dict_content = {"content": content}
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
            for i in range(len(w)) :
                stop_words.append(w[i])
        else :
            for i in range(len(w)-1) :
                d+=w[i]+"_"
            d+=w[len(w)-1]
            stop_words.append(d)

    for d in data_pos :
        for w in d['content_postag'] :
            if(d['content_postag'][w] in pos ) :
                stop_words.append(w)
    # print(stop_words)
    return stop_words


doc_set = getData()
stop_words = loadStopwords()

texts = []
#
for d in doc_set:
    d = d['content']
    raw = d.lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = []
    for w in tokens:
        word = w
        for i in range(len(w)):
            if (w[i] == "_"):
                word = w[:i] + " " + w[i + 1:]
        if not word in stop_words:
            if (len(word) > 2):
                stopped_tokens.append(w)
    texts.append(stopped_tokens)
#
# print(texts)

model = gensim.models.Word2Vec(texts, min_count=1)
model.save("model.w2v")
# model = gensim.models.Word2Vec.load("model.w2v")
# vector = model.most_similar("ý_kiến".split())
# print(vector)