from __future__ import absolute_import
from __future__ import print_function
from nltk.tokenize import word_tokenize
import csv
from data_access  import *
import rake
import rake_v2


limit = 10000
# file_path = "data/data_news_soha_10000.csv"
stoppath = "data/stoplists/vietnamese-stopwords.txt"


def get_all_data(limit):
    data = []
    with open('data/data_news_soha.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id':row['newsId']}
            content = row['title_token'].lower() + " "+ row['sapo_token'].lower() +" "+row['content_token'].lower()
            dict_content = {"content" : content}
            dict.update(dict_content)
            data.append(dict)
    return data[0:limit]

def load_all_tfidf() :
    word_tfidf = []
    with open('tf-idf_v2.txt') as fp:
        for row in range(0,limit) :
            line = fp.readline().split(" ")
            word_tfidf.append(line)
    return word_tfidf

def run():
    data = get_all_data(limit)
    # keywords = []
    tf_idf = load_all_tfidf()
    file = open('rake.txt', 'w')
    for index in range(len(data)):
        word_tf = []
        word = []
        # key = {}
        # key.update({'id': data[index]['id']})
        # print("id : "+data[index]['id']+" ")

        file.write(str(data[index]['id'] + ":"))
        keys = run_rake(stoppath,data[index]['content'],data[index]['id'])
        # print(data[index]['content'])

        for i in range(len(keys)):
            word.append(keys.__getitem__(i)[0])
            file.write(keys.__getitem__(i)[0]+",")
        file.write("\n")

        print(word)
        print(len(tf_idf[index]))
        for j in range(10,len(tf_idf[index])):
            tup = tf_idf[index][j].split(":")
            word_tf.append(tup[0])
        move = [w for w in word if w in word_tf]
        print(move)
        result = [w for w in word if w not in move]
        print("result: ", result,"\n")

        # keyword = {'keyword': word}
    #
    #     key.update(keyword)
    #     keywords.append(key)
    #
    # for k in keywords:
    #     file.write(str(data[index]['id'] + " " + str(k['keyword']) + "\n")
        # print(k['id'], k['keyword'])

#######################################################################

def get_content_Id(id):
    row = get_token(id)
    title = row['title_token']
    link = get_news(id)['url']
    content = title.lower() + " "+ row['sapo_token'].lower() +" "+row['content_token'].lower()

    return content,title,link


def get_tfidf(id) :
    word_tfidf = []
    with open('tf-idf.txt') as fp:
        for row in range(0,limit) :
            line = fp.readline().split(" ")
            if id ==line[0] :
                word_tfidf = line[1:]
                break
    return word_tfidf


def run_rake(stop_path,text, id) :
    rake_object = rake.Rake(5, 2, 2)
    keywords = rake_object.run(stop_path,text = text, id=id)
    return keywords


def run_api(id) :
    content, title, link = get_content_Id(id)

    tf_idf = get_tfidf(id)

    word_tf = []
    word = []

    keys = run_rake(stoppath,content,id)
    print(keys)
    for i in range(len(keys)):
        word.append(keys.__getitem__(i)[0])

    for j in range(10, len(tf_idf)):
        tup = tf_idf[j].split(":")
        word_tf.append(tup[0])

    move = [w for w in word if w in word_tf]
    print(move)
    result = [w for w in word if w not in move]
    print("result: ", result, "\n")
    return  result , title, link


# def get_news(id):
#     tags = run_api(id)
#     allTags = []
#     with open('rake.txt') as file :
#         for row in range(len(file)):
#             line = file.readline().split(":")



if __name__ == '__main__' :

    id = "20180711155637607"
    run_api(id)
    # run()
    # get_news(id)



