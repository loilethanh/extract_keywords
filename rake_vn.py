from __future__ import absolute_import
from __future__ import print_function
from nltk.tokenize import word_tokenize
from rake import *
from tfidf import *
import csv
from data_access  import *
import rake
import rake_v2

tf_idf_file = './result/tf-idf_ngram.txt'
limit = 100
file_path = "data/data_news_soha.csv"
stoppath = "data/stoplists/vietnamese-stopwords.txt"

def run_rake(stop_path,text, aid ) :
    rake_object = rake.Rake(5, 3, 2)
    keywords = rake_object.run(stop_path,text = text, id=aid)
    return keywords



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

# def run():
#     data = get_all_data()
#     tf_idf = load_all_tfidf()
#
#     file = open('result/rake_remove.txt', 'w')
#     for index in range(len(data)):
#         word_remove = []
#         word_key = []
#         file.write(str(data[index]['id'] + ":"))
#         keys = run_rake(stoppath,data[index]['content'],data[index]['id'])
#         print("keys:", keys)
#         for i in range(len(keys)):
#             word_key.append(keys.__getitem__(i)[0])
#
#         print("lenght word :", len(tf_idf[index]))
#         for j in range(int(len(tf_idf[index])/5),len(tf_idf[index])):
#             sub = tf_idf[index][j].split(":")
#             word_remove.append(sub[0])
#
#         move = [w for w in word_key if w in word_remove]
#         print("remove : ", move)
#         result = [w for w in word_key if w not in move]
#         print("result : ", result,"\n" )
#
#
#         for w in result :
#             file.write(str(w)+",")
#         file.write("\n")

def load_all_tfidf() :
    word_tfidf = []
    with open(tf_idf_file) as fp:
        for row in range(0,limit) :
            line = fp.readline().split(",")
            word_tfidf.append(line)
    return word_tfidf

def run_tfidf():
    data = get_all_data()
    tf_idf = load_all_tfidf()

    file = open('result/rake_ngram_V.txt', 'w')
    for index in range(len(data)):
        file.write(str(data[index]['id'] + ":"))
        print(data[index]['id'])
        result = []
        keys = run_rake(stoppath, data[index]['content'], data[index]['id'])
        print("keys", keys)
        for i in range(len(keys)):
            w = keys.__getitem__(i)
            for j in range(len(tf_idf[index])):
                sub = tf_idf[index][j].split(":")
                if w[0] == sub[0] :
                    result.append((w[0],float(w[1]) * float(sub[1])))

        result.sort(key=lambda  x: x[1], reverse= True)
        print(result)

        for w in result:
            file.write(str(w) + ",")
        file.write("\n")
        print("\n")


# def remove_key(id, keys):
#     result = []
#     postag  = load_postag(id)
#     print(postag)
#
#     rule = {'N-V','N-N-V'}

#######################################################################


def get_content_Id(aid):

    row = get_token(aid)
    title = row['title_token'].lower()
    link = get_news(aid)['url']
    content = title + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()

    return content,title,link


def get_tfidf_(aid) :
    alive = False
    word_tfidf = []
    with open(tf_idf_file) as fp:
        for row in range(0,limit) :
            line = fp.readline().split(",")
            if aid ==line[0] :
                word_tfidf = line[1:]
                alive = True
                break
    if not alive :
        tfidf = get_tf_idf(aid)
        for d in tfidf :
            word_tfidf.append(str(d[0])+":"+str(d[1]))

    return word_tfidf


def run_api(id) :

    content, title, link = get_content_Id(id)
    result= []
    tf_idf = get_tfidf_(id)
    print(tf_idf)
    keys = run_rake(stoppath, content, id)

    print("key:", len(keys),keys)
    for i in range(len(keys)):
        w = keys.__getitem__(i)
        for j in range(len(tf_idf)):
            sub = tf_idf[j].split(":")
            if w[0] == sub[0]:
                result.append((w[0], float(w[1]) * float(sub[1])))
    result.sort(key=lambda x: x[1], reverse=True)
    print(len(result), result," ",)
    return  result , title, link

def get_tags_entity(id):

    pass

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
    # run()
    id = "20180618151347251"
    # remove_key(id,[])
    run_api(id)
    # run_tfidf()
#     # a = get_content_Id(id)
#     # print(a)
#     run_api_remove(20180723200916257)
#     get_new(id)
#     get_content_Id(id)
#     get_tfidf(id)



