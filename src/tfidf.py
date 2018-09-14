import time
from nltk.tokenize import RegexpTokenizer
import csv
from nltk.tokenize import word_tokenize
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from src.data_access import *
from setup import *

tokenizer = RegexpTokenizer(r'\w+')


def load_model(file):
    start = time.time()
    with open(file, 'rb') as f:
        model = pickle.load(f)
    print("load model", time.time() - start)
    start= time.time()
    feature_names = model.get_feature_names()
    print("load feature_names", time.time() - start)

    return model,feature_names

def norm (numbers) :
    a = math.sqrt(numbers)
    return 1.0/a


def getData():
    news = get_news_update()
    data =[]
    for row in news:
        dict = {
                'id': str(row['news_id']),
                'title': str(row['title_token']).lower(),
                "content": str(row['sapo_token']).lower()
                           + " " + str(row['content_token']).lower(),
                'insertDate': row['insertDate'],
                }
        data.append(dict)
    return data


def load_stopwords_tfidf(file):
    stop_words = []
    for x in open(file, 'r').read().split('\n'):
        d = ''
        w = x.split(" ")
        if len(w)== 1 :
            stop_words.append(w[0])
        else :
            for i in range(len(w)-1) :
                d += w[i]+"_"
            d+=w[len(w)-1]
            stop_words.append(d)
    return stop_words


def get_corpus(doc_set,stop_words):
    texts = []
    for d in doc_set:
        tokens = tokenizer.tokenize(d['title'] + " " + d['content'])
        stopped_tokens= [word for word in tokens if not word in stop_words]
        string = ''
        for word in stopped_tokens:
            string += word + " "
        texts.append(string)
    return  texts


def build_models(doc_set,file_save, save_option= False):
    # doc_set = getData(date)
    stop_words = load_stopwords_tfidf(stoppath)
    texts = get_corpus(doc_set,stop_words)

    model = TfidfVectorizer(analyzer='word', ngram_range=(1,3),
             stop_words=stop_words,min_df= 3 , max_df = 0.01,)

    tfidf_matrix = model.fit_transform(texts)
    feature_names = model.get_feature_names()
    result = []

    for index in range(len(doc_set)):
        feature_index = tfidf_matrix[index, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [tfidf_matrix[index, x] for x in feature_index])
        res = []
        for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
            if ( w in doc_set[index]['title'] ):
                res.append((str(w), s * norm(len(doc_set[index]['title']))))
            if ((w in doc_set[index]['content']) and (w not in doc_set[index]['title'] ) and(norm(len(doc_set[index]['content'])) != 0 )):
                res.append((str(w), s * norm(len(doc_set[index]['content']))))
        res.sort(key=lambda x: x[1], reverse=True)
        result.append(res)

    if save_option == True :
        with open(file_save, 'wb') as f:
            pickle.dump(model, f)


def get_tf_idf(stop_words,contents, model ,feature_names) :

    # row = get_token(id)
    title = contents['title']
    content = contents['content']
    norm_title = norm(len(title))
    norm_content = norm(len(content))
    tokens = tokenizer.tokenize(title +" "+content)
    stopped_tokens = [word for word in tokens if not word in stop_words]
    string = ''
    for word in stopped_tokens:
        string += word + " "
    str = [string]
    tfidf_matrix = model.transform(str)
    feature_index = tfidf_matrix.nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[0, x] for x in feature_index])

    result = []
    for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
        if w in (title) :
            result.append((w, s * norm_title))
        if ((w in content) and (w not in title) and (norm(len(content)) > 0)):
            result.append((w, s * norm_content))

    result.sort(key=lambda x: x[1], reverse=True)


    return result


