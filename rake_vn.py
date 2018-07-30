from __future__ import absolute_import
from __future__ import print_function
from nltk.tokenize import word_tokenize
from rake import *
from tfidf import *
import csv
from data_access  import *
import rake
import rake_v2


threshold = 5
tf_idf_file = './result/tf-idf_ngram.txt'
limit = 10
file_path = "data/data_news_soha.csv"
stoppath = "data/stoplists/vietnamese-stopwords.txt"
file_ = 'result/rake_ngram.txt'

def run_rake(stop_path,text, aid,) :
    rake_object = rake.Rake(5,3,2)
    keywords = rake_object.run(stop_path,text = text, id=aid)
    return keywords

# def get_all_data():
#     data = []
#     with open(file_path) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             dict = {'id':str(row['newsId'])}
#             content = str(row['title_token']).lower() + " "+ str(row['sapo_token']).lower() +" "+str(row['content_token']).lower()
#             dict_content = {"content" : content}
#             dict.update(dict_content)
#             data.append(dict)
#     return data[0:limit]
#
# #
# def load_all_tfidf() :
#     word_tfidf = []
#     with open(tf_idf_file) as fp:
#         for row in range(0,limit) :
#             line = fp.readline().split(",")
#             word_tfidf.append(line)
#     return word_tfidf
# #
# # def write_file(id, option , result):
# #     file = open(file_, 'w')
# #     file.write(str(id) + ",")
# #     if option:
# #         for r in result:
# #             file.write(str(r[0]) + ":" + str(r[1]) + ",")
# #     else :
# #         for r in result:
# #             file.write(str(r[0])+",")
# #     file.write("\n")
#
# #
#
# def run( option_value = True, write = False ):
#     data = get_all_data()
#     tf_idf = load_all_tfidf()
#     file = open(file_, 'w')
#     for index in range(len(data)):
#         # print(data[index]['id'])
#         result = []
#         keys = run_rake(stoppath, data[index]['content'], data[index]['id'])
#         # print("keys", keys)
#         # if len(keys) > 4 :
#         #     thr = threshold
#         # else: thr = len(keys)
#         for i in range(0,len(keys)):
#             w = keys.__getitem__(i)
#             for j in range(len(tf_idf[index])):
#                 sub = tf_idf[index][j].split(":")
#                 if w[0] == sub[0] :
#                     result.append((w[0],float(w[1]) * float(sub[1])))
#
#         result.sort(key=lambda  x: x[1], reverse= True)
#         # print(result)
#         # print("\n")
#         file.write(str(data[index]['id']) + ",")
#         if option_value:
#             for r in result:
#                 file.write(str(r[0]) + ":" + str(r[1]) + ",")
#         else:
#             for r in result:
#                 file.write(str(r[0]) + ",")
#         file.write("\n")
#
#         # if data[index]['id'] == "20161222173627577" :
#         #     print(data[index]['content'])
#
#         # if write :
#         #     write_file(data[index]['id'],option,result)


#######################################################################


def get_content_id(aid):

    row = get_token(aid)
    title = row['title_token'].lower()
    link = get_news(aid)['url']
    content = title + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()
    content_PoS = load_postag(aid)
    tag = row["tag_postag"]

    return content,title,link,tag,content_PoS


def get_tfidf_(aid) :
    word_tfidf = []
    tfidf = get_tf_idf(aid)
    for d in tfidf:
        word_tfidf.append(str(d[0]) + ":" + str(d[1]))

    return word_tfidf


# check tag in the content of news
def check_postag(tags, content):
    tag_pos = tags.split(" ")
    tokens = word_tokenize(content)
    content_postag = []
    for t in tag_pos:
        print(t)
        w = ''
        postag = ''
        for i in range(len(t)):
            if t[-i] == "/":
                w = t[-len(t):-i].lower()
                postag = t[-i + 1:]
                print(postag)
                break
        if (postag == "Np" and w in tokens and w not in content_postag ):
            content_postag.append(w)

    print("postag",content_postag)

    return  content_postag


#check PoS of keyword
def check_keyword(result):
    results = []
    return results


def run_api(option,id) :
    content, title, link,tags,content_PoS = get_content_id(id)
    content_postag = check_postag(tags, content)
    result= []
    tf_idf = get_tfidf_(id)
    tag= []
    # print(tf_idf)
    keys = run_rake(stoppath, content, id)

    # print("key:", len(keys),keys)
    for i in range(len(keys)):
        w = keys.__getitem__(i)
        for j in range(len(tf_idf)):
            sub = tf_idf[j].split(":")
            if w[0] == sub[0]:
                result.append((w[0], float(w[1]) * float(sub[1])))
            # if w[0] in content_postag and w[0] not in check :
            #     tag.append(w[0])
    result.sort(key=lambda x: x[1], reverse=True)


    if len(keys) > threshold-1:
        thr = threshold
    else: thr = len(keys)
    print(thr)
    result = result[:thr]
    print(len(result))
    for r in result :
        tag.append(r[0])
    print("tag",tag)
    # test = [w for w in content_postag and w in check]

    check = [tg for tg in content_postag if tg not in tag ]
    print("check",check)
    result = tag + check
    if option:
        print(len(result), result," ",)
    print(title,link)
    return  result , title, link

# def get_new(aid):
#     tags_news, title, link  = run_api(aid)
#     print(tags_news)
#     news=[]
#     # news_ids=[]
#
#     with open('rake.txt') as fp:
#         for row in range(0,limit) :
#             line = fp.readline().split(":")
#
#             # news_ids.append(line[0])
#             # news_tag, new_title, new_link = get_content_Id(line[0])
#             news_tag = line[1]
#             # print(news_tag)
#             # new_title = get_token(line[0])
#             # new_link = get_news(line[0])['url']
#             result = {}
#             #
#             join = [t for t in tags_news if t in news_tag]
#             if len(join) > 0:
#             #     # print(news_ids[row], ":", join)
#             #     result.update({"id": line[0],"title":new_title,"link": new_link,"keyword" : join})
#                 result.update({"id": line[0],"keyword" : join})
#                 print(result)
#                 news.append(result)
#
#     return news

if __name__ == '__main__' :
    start = time.time()
    id = "20180728132548725"
    run_api(True,id)
    # run(False,True)

    print("--- %s seconds ---" % (time.time() - start))


