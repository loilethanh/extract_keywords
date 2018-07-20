from gensim.models import TfidfModel
from gensim import models, corpora
from nltk.tokenize import RegexpTokenizer
import csv,gensim
from nltk.tokenize import word_tokenize
import math
from data_access  import *

from sklearn.feature_extraction.text import TfidfVectorizer

tokenizer = RegexpTokenizer(r'\w+')
file_path = "data/data_news_soha.csv"

limit = 1000

def norm (numbers) :
    a = math.sqrt(numbers)
    return 1/a



def getData():
    data=[]
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id':str(row['newsId'])}
            dict.update({'title' :str(row['title_token']).lower()})
            content = str(row['sapo_token']).lower() +" "+str(row['content_token']).lower()
            # print(content)
            dict.update({"content" : content})
            data.append(dict)
    return data[0:limit]


def load_postag ():
    data_postag = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in  reader :
            id = str(row['newsId'])
            content =str(row['title_postag'])+" "+str(row['sapo_postag'])+" "+str(row['content_postag'])
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

    return data_postag[0:limit]


def loadStopwords():
    data_pos = load_postag()
    pos = ['C', 'Cc', 'M', 'A', 'E', 'M', 'R',  'T', 'X']
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


def run() :
    doc_set = getData()
    stop_words = loadStopwords()
    texts = []
    texts_title = []
    texts_content = []

    for d in doc_set:
        tokens_title = tokenizer.tokenize(d['title'])
        tokens_content = tokenizer.tokenize(d['content'])
        # tokens = tokens_title + tokens_content

        stopped_tokens_title = []
        stopped_tokens_content = []
        stopped_tokens = []
        # for word in tokens:
        #     w = word.lower()
        #     if not w in stop_words:
        #         stopped_tokens.append(w)
        for word in tokens_title:
            w = word.lower()
            if not w in stop_words:
                stopped_tokens_title.append(w)
        for word in tokens_content:
            w = word.lower()
            if not w in stop_words:
                stopped_tokens_content.append(w)
        stopped_tokens = stopped_tokens_title + stopped_tokens_content

        texts.append(stopped_tokens)
        texts_content.append(stopped_tokens_content)
        texts_title.append(stopped_tokens_title)

    dictionary = corpora.Dictionary(texts)
    #
    # dictionary.filter_extremes(no_below=1, no_above=0.03)
    # # token2ids = dictionary.token2id.items()
    corpus = [dictionary.doc2bow(text) for text in texts]

    models = TfidfModel(corpus)
    file = open('result/tf-idf.txt', 'w')

    for i in range(len(doc_set)):

        file.write(str(doc_set[i]['id']) + " ")

        vector = models[corpus[i]]
        result = []
        for id, val in vector:
            if dictionary.get(id) in texts_title[i]:
                result.append((dictionary.get(id), val * norm(len(texts_title[i]))))

            if ((dictionary.get(id) in texts_content[i]) and (dictionary.get(id) not in texts_title[i])):
                result.append((dictionary.get(id), val * norm(len(texts_content[i]))))
        result.sort(key=lambda x: x[1], reverse=True)

        for r in result:
            file.write(r[0] + ":" + str(r[1]) + " ")
        file.write("\n")

if __name__=="__main__" :
    run()
    # getData()
    # load_postag()
    # loadStopwords()

