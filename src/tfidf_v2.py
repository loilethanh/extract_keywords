import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim import  corpora
from nltk.util import ngrams
from src.tfidf import *
from setup import *

tokenizer = RegexpTokenizer(r'\w+')


def norm_ (numbers) :
    a = math.sqrt(numbers)
    return 1.0/a


def load_stopwords_tfidf_(file):
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


# def get_lastdate_update_():
#
#     file  = open(file_update,"r")
#     date = file.read()
#     print(date)
#     file.close()
#     return date
#
# def write_file_(date) :
#     try:
#         file = open(file_update,"w")
#         file.write(str(date))
#         file.close()
#         print("Done !")
#     except Exception as e :
#         print(e)

def word_grams(words, min=1, max=3):
    results = []
    for n in range(min, max+1):
        for ngram in ngrams(words, n):
            results.append(' '.join(str(i) for i in ngram))
    return results


def get_data_(doc_set,stop_words):
    data =[]
    for d in doc_set:
        tokens = tokenizer.tokenize(d['title'] + " " + d['content'])
        stopped_tokens = [word for word in tokens if not word in stop_words]
        results = word_grams(stopped_tokens)
        data.append(results)
    return data


def build_dict(doc_set,stop_words):
    data = get_data_(doc_set,stop_words)
    dictionary = Dictionary(data)
    dictionary.save(dictionary_file)
    print("Save dictionary !:", dictionary)
    models = TfidfModel(dictionary=dictionary)
    models.save(model_tfidf_file)
    print("Save models!")
    return dictionary,models


def update_dict(doc_set, dictionary,stop_words):
    data_set = get_data_(doc_set,stop_words)
    dictionary.add_documents(data_set)
    models = TfidfModel(dictionary=dictionary)

    try :
         dictionary.save(dictionary_file)
         models.save(model_tfidf_file)
         print("Update Dictionary and Model successful !")
    except Exception as e :
        print(e)
    # return dictionary,models

# def build_models(dictionary):
#     models = TfidfModel(dictionary= dictionary)
#     models.save("models.tfidf")
#     return models


def get_tfidf(stop_words,contents , models,dictionary ):
    start = time.time()
    title = contents['title']
    content = contents['content']

    norm_title = norm(len(title))
    norm_content = norm(len(content))

    tokens = tokenizer.tokenize(title+" "+content)
    token_word = [ word for word in tokens if not word in stop_words]
    words = word_grams(token_word)
    dictionary.add_documents([words])

    corpus_doc = dictionary.doc2bow(words)
    vector = models[corpus_doc]
    print("time get :",time.time() - start)

    start = time.time()
    result = []
    for id, value in vector:
        word = dictionary.get(id)
        print(word,value)
        if word in title :
            result.append((word,value * norm_title))
        if (word in content and word not in title) and (norm_content > 0):
            result.append((word,value * norm_content))

    print("time get calculator :",time.time() - start)
    return result


def get_content_(date):
    """
    get data from db
    :return:
    """
    news = get_news_update(date)
    data = []
    for row in news:
        dict = {'id': str(row['news_id']),
                'title': str(row['title_token']).lower(),
                "content": str(row['sapo_token']).lower()
                           + " " + str(row['content_token']).lower() ,
                'insertDate':row['insertDate'],
                }
        data.append(dict)

    return data


def load_model_v2():
    start = time.time()
    models = TfidfModel.load(model_tfidf_file)
    print("Time for load models : ",time.time()- start)
    start = time.time()
    dict = Dictionary.load(dictionary_file)
    print("Time for load dictionary : ",time.time()- start)

    return models,dict







