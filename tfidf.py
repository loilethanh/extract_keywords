import time
from gensim.models import TfidfModel
from gensim import models, corpora
from nltk.tokenize import RegexpTokenizer
import csv,gensim
from nltk.tokenize import word_tokenize
import math
from data_access  import *

from sklearn.feature_extraction.text import TfidfVectorizer

tokenizer = RegexpTokenizer(r'\w+')
file_path = "data/data_news_soha_10000.csv"
file_write = "result/tf-idf_ngram_10000"
limit = 10000

def norm (numbers) :
    a = math.sqrt(numbers)
    return 1/a

def getData():
    data=[]
    data_postag = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id':str(row['newsId']) ,
                    'title': str(row['title_token']).lower() + " " + str(row['sapo_token']).lower(),
                    "content": str(row['content_token']).lower()}
            data.append(dict)


            content_pos = str(row['title_postag']) + " " + str(row['sapo_postag']) + " " + str(row['content_postag'])
            content_postag = {}
            word_tokens = word_tokenize(content_pos)
            for word in word_tokens:
                w = ''
                postag = ''
                for i in range(len(word)):
                    if word[-i] == "/":
                        w = word[-len(word):-i].lower()
                        postag = word[-i + 1:]
                        break
                content_postag.update({w: postag})
            data_postag.append({'id': id, 'content_postag': content_postag})

    return data[0:limit],data_postag[0:limit]


# def load_postag ():
#     data_postag = []
#     with open(file_path) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in  reader :
#             id = str(row['newsId'])
#             content =str(row['title_postag'])+" "+str(row['sapo_postag'])+" "+str(row['content_postag'])
#             content_postag ={}
#             word_tokens = word_tokenize(content)
#             for word in word_tokens :
#                 w = ''
#                 postag = ''
#                 for i in range(len(word)):
#                     if word[-i] == "/" :
#                         w = word[-len(word):-i].lower()
#                         postag = word[-i+1:]
#                         break
#                 content_postag.update({w:postag})
#             data_postag.append({'id':id,'content_postag':content_postag})
#
#     return data_postag[0:limit]


def load_stopwords(data_pos):
    pos = ['C', 'Cc','A','M', 'E', 'R',  'T', 'X']
    stop_words = []
    for x in open('data/stoplists/vietnamese-stopwords.txt', 'r').read().split('\n'):
        d = ''
        w = x.split(" ")
        if len(w)== 1 :
            stop_words.append(w[0])
        else :
            for i in range(len(w)-1) :
                d += w[i]+"_"
            d+=w[len(w)-1]
            stop_words.append(d)

    for d in data_pos :
        for w in d['content_postag'] :
            if(d['content_postag'][w] in pos ) :
                stop_words.append(w)
    return stop_words


# def run() :
#     doc_set = getData()
#     stop_words = load_stopwords()
#     texts = []
#
#     for d in doc_set:
#         tokens = tokenizer.tokenize(d['title']+" "+d['content'])
#         stopped_tokens= [word for word in tokens if not word in stop_words]
#         texts.append(stopped_tokens)
#
#     dictionary = corpora.Dictionary(texts)
#     # dictionary.filter_extremes(no_below=1, no_above=0.03)
#     corpus = [dictionary.doc2bow(text) for text in texts]
#     models = TfidfModel(corpus)
#     file = open('result/tf-idf.txt', 'w')
#
#     for i in range(len(doc_set)):
#         file.write(str(doc_set[i]['id']) + ",")
#         vector = models[corpus[i]]
#         result = []
#         for id, val in vector:
#             if dictionary.get(id) in doc_set[i]['title']:
#                 result.append((dictionary.get(id), val * norm(len(doc_set[i]['title']))))
#
#             if ((dictionary.get(id) in doc_set[i]['content']) and (dictionary.get(id) not in doc_set[i]['title'])):
#                 result.append((dictionary.get(id), val * norm(len(doc_set[i]['content']))))
#         result.sort(key=lambda x: x[1], reverse=True)
#
#         for r in result:
#             file.write(r[0] + ":" + str(r[1]) + ",")
#         file.write("\n")

def write_file(doc_set, result):
    file = open(file_write, 'w')
    for i in range(len(result)):
        file.write(str(doc_set[i]['id']) + ",")
        for r in result[i]:
            file.write(r[0] + ":" + str(r[1]) + ",")
        file.write("\n")


def get_corpus(doc_set,stop_words):
    texts = []
    for d in doc_set:
        tokens = tokenizer.tokenize(d['title'] + " " + d['content'])
        stopped_tokens= [word for word in tokens if not word in stop_words]
        string = ''
        for word in stopped_tokens:
            string +=word+" "
        texts.append(string)
    return  texts


def run_ngram():
    doc_set,data_pos = getData()
    stop_words = load_stopwords(data_pos)
    texts = get_corpus(doc_set,stop_words)

    model = TfidfVectorizer(analyzer='word', ngram_range=(1,3),stop_words=stop_words)
    tfidf_matrix = model.fit_transform(texts)
    feature_names = model.get_feature_names()
    result = []

    for index in range(len(doc_set)):
        feature_index = tfidf_matrix[index, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [tfidf_matrix[index, x] for x in feature_index])
        res = []
        for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
            if (w in doc_set[index]['title']  ):
                res.append((str(w), s * norm(len(doc_set[index]['title']))))

            if ((w in doc_set[index]['content']) and (w not in doc_set[index]['title'] ) and(norm(len(doc_set[index]['content'])) != 0 )):
                res.append((str(w), s * norm(len(doc_set[index]['content']))))
        res.sort(key=lambda x: x[1], reverse=True)
        result.append(res)

    write_file(doc_set, result)


def get_tf_idf(id) :

    doc_set = getData()
    stop_words = load_stopwords()
    texts = get_corpus(doc_set, stop_words)

    row = get_token(id)
    title = row['title_token'].lower()
    content = title + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()

    tokens = tokenizer.tokenize(content)
    stopped_tokens = [word for word in tokens if not word in stop_words]
    string = ''
    for word in stopped_tokens:
        string += word + " "

    str = [string]

    model = TfidfVectorizer(analyzer='word', ngram_range=(1,3),stop_words=stop_words)
    # model.fit(texts)


    tfidf_matrix = model.fit_transform(str)

    feature_names = model.get_feature_names()
    feature_index = tfidf_matrix.nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[0, x] for x in feature_index])

    result = []
    for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
        # print(w, s)
        if w in (row['title_token'].lower()+row['sapo_token'].lower()) :
            result.append((w, s * norm(len(row['title_token']+row['sapo_token']))))
        if ((w in row['content_token']) and (w not in row['title_token']) and (
                norm(len(row['content_token'])) != 0)):
            result.append((w, s * norm(len(['content_token']))))

    result.sort(key=lambda x: x[1], reverse=True)
    # print(result)

    return result




if __name__=="__main__" :
    start = time.time()
    # run_ngram()
    # get_tf_idf(20180725011933491)

    print("--- %s seconds ---" % (time.time() - start))
    # run()
    # getData()
    # load_postag()
    # loadStopwords()

