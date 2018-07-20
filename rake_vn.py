from __future__ import absolute_import
from __future__ import print_function
from nltk.tokenize import word_tokenize
import csv
from data_access  import *
import rake
import rake_v2


limit = 1000
file_path = "data/data_news_soha.csv"
stoppath = "data/stoplists/vietnamese-stopwords.txt"


def get_all_data():
    data = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict = {'id':str(row['newsId'])}
            content = str(row['title_token']).lower() + " "+ str(row['sapo_token']).lower() +" "+str(row['content_token']).lower()
            dict_content = {"content" : content}
            dict.update(dict_content)
            data.append(dict)
    return data[0:limit]

def load_all_tfidf() :
    word_tfidf = []
    with open('result/tf-idf.txt') as fp:
        for row in range(0,limit) :
            line = fp.readline().split(" ")
            word_tfidf.append(line)
    # print(word_tfidf)
    return word_tfidf

def run():
    data = get_all_data()
    tf_idf = load_all_tfidf()
    file = open('result/rake_v1.txt', 'w')
    for index in range(len(data)):
        word_remove = []
        word = []
        # print(data[index]['id'],"\n")
        file.write(str(data[index]['id'] + ":"))
        keys = run_rake(stoppath,data[index]['content'],data[index]['id'])
        # print(keys,"\n")
        for i in range(len(keys)):
            word.append(keys.__getitem__(i)[0])

        for j in range(10,len(tf_idf[index])):
            sub = tf_idf[index][j].split(":")
            word_remove.append(sub[0])

        move = [w for w in word if w in word_remove]
        # print("remove : ", move)
        result = [w for w in word if w not in move]
        # print("result : ", result )

        for w in result :
            file.write(str(w)+",")
        file.write("\n")


#######################################################################

def get_content_Id(aid):

    # row = get_token(aid)
    # title = row['title_token']
    # link = get_news(aid)['url']
    # content = title.lower() + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['newsId'] == aid :
                title = row['title_token']
                # link = get_news(aid)['url']
                link = row['url']
                content = title.lower() + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()
    # print(content)
    return content,title,link


def get_tfidf(aid) :
    word_tfidf = []
    with open('./result/tf-idf.txt') as fp:
        for row in range(0,limit) :
            line = fp.readline().split(" ")
            if aid ==line[0] :
                word_tfidf = line[1:]
                break
    # print(word_tfidf)
    return word_tfidf


def run_rake(stop_path,text, aid ) :
    rake_object = rake.Rake(5, 3, 2)
    keywords = rake_object.run(stop_path,text = text, id=aid)
    return keywords


def run_api(aid) :
    content, title, link = get_content_Id(aid)

    tf_idf = get_tfidf(aid)

    word_tf = []
    word = []

    keys = run_rake(stoppath,content,aid)
    print(keys)

    for i in range(len(keys)):
        word.append(keys.__getitem__(i)[0])
    for j in range(int(len(tf_idf)/10), len(tf_idf)):
        tup = tf_idf[j].split(":")
        word_tf.append(tup[0])
    print(word_tf)
    move = [w for w in word if w in word_tf]
    print("move",move)
    result = [w for w in word if w not in move]
    print("result: ", result, "\n")
    return  result , title, link


def get_new(aid):
    tags_news, title, link  = run_api(aid)
    print(tags_news)
    news=[]
    # news_ids=[]

    with open('rake.txt') as fp:
        for row in range(0,limit) :
            line = fp.readline().split(":")

            # news_ids.append(line[0])
            # news_tag, new_title, new_link = get_content_Id(line[0])
            news_tag = line[1]
            # print(news_tag)
            # new_title = get_token(line[0])
            # new_link = get_news(line[0])['url']
            result = {}
            #
            join = [t for t in tags_news if t in news_tag]
            if len(join) > 0:
            #     # print(news_ids[row], ":", join)
            #     result.update({"id": line[0],"title":new_title,"link": new_link,"keyword" : join})
                result.update({"id": line[0],"keyword" : join})
                print(result)
                news.append(result)

    return news

if __name__ == '__main__' :
    run()
    # id = "20180618152537063"
#     # a = get_content_Id(id)
#     # print(a)
#     run_api(id)
#     get_new(id)
#     get_content_Id(id)
#     get_tfidf(id)



