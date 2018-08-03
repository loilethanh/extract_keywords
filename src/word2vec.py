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

limit = 1000

def getData():
    data = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id': row['newsId']}
            content = row['title_token'].lower() + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()
            dict_content = {"content": content}
            dict.update(dict_content)
            data.append(dict)
    return data[0:limit]


def load_postag ():
    data_postag = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in  reader :
            id = row['newsId']
            content =row['title_postag']+" "+row['sapo_postag']+" "+row['content_postag']
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


def run():
    doc_set = getData()
    stop_words = loadStopwords()

    texts = []
    #
    for d in doc_set:
        tokens = tokenizer.tokenize(d['content'])
        stopped_tokens = [w for w in tokens if w not in stop_words]
        texts.append(stopped_tokens)
    #
    # print(texts)

    # model = gensim.models.Word2Vec(texts, min_count=1)
    # model.save("model.w2v")
    model = gensim.models.Word2Vec.load("model.w2v")
    # vector = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
    vector = model.similarity("minh_beo")
    print(vector)
if __name__ == '__main__':
    run()