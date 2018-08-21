import time
from nltk.tokenize import RegexpTokenizer
import csv
from nltk.tokenize import word_tokenize
import math

from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


tokenizer = RegexpTokenizer(r'\w+')
file_path = "../data/data_news_soha_10000.csv"
# file_write = "models/tf-idf.txt"
file_model ="../models/vectorizer.pk"
file_stopwords = '../data/stoplists/vietnamese-stopwords.txt'
# file_stopwords = '../data/stoplists/words.txt'
# limit = 1000

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
    data=[]
    data_postag = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id':str(row['newsId']) ,
                    'title': str(row['title_token']).lower() ,
                    "content":  str(row['sapo_token']).lower() + " " + str(row['content_token']).lower()}
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
            data_postag.append({'id': str(row['newsId']), 'content_postag': content_postag})

    return data ,data_postag

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
            string +=word+" "
        texts.append(string)
    return  texts


def run_ngram(save_option= False ):
    doc_set,data_pos = getData()
    stop_words = load_stopwords_tfidf(file_stopwords)
    texts = get_corpus(doc_set,stop_words)

    model = TfidfVectorizer(analyzer='word', ngram_range=(1,3),stop_words=stop_words,min_df=1)
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

    if save_option == True :
        with open('../models/vectorizer_word.pk', 'wb') as f:
            pickle.dump(model, f)


def get_tf_idf(stop_words,contents, model ,feature_names) :

    # row = get_token(id)
    title = contents['title']
    content =contents['content']

    tokens = tokenizer.tokenize(title+" "+content)
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
            result.append((w, s * norm(len(title))))
        if ((w in content) and (w not in title) and (norm(len(content)) != 0)):
            result.append((w, s * norm(len(content))))

    result.sort(key=lambda x: x[1], reverse=True)


    return result

#
if __name__=="__main__" :
    start = time.time()
    # model,feature_names = load_model(file_model)
    run_ngram(save_option=True)
#     # get_tf_idf(20180731122004553,model,feature_names)
    print("--- %s seconds ---" % (time.time() - start))
    # run()
    # getData()
    # load_postag()
    # loadStopwords()

