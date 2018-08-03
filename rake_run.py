from __future__ import absolute_import
from __future__ import print_function
from nltk.tokenize import word_tokenize
from rake import *
from tfidf import *
import csv
from data_access  import *
import rake, time
import rake_v2


threshold = 5
# tf_idf_file = './result/tf-idf_ngram.txt'
file_path = "data/data_news_soha_10000.csv"
stoppath = "data/stoplists/vietnamese-stopwords.txt"
file_ = 'result/rake_ngram.txt'
file_model = 'result/vectorizer.pk'


def run_rake(stop_path,text,content) :

    rake_object = rake.Rake(5,3,2)
    keywords = rake_object.run(stop_path,text = text,content_pos= content)
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
#     return data[3:10]
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
# def write_file(id, option , result):
#     file = open(file_, 'w')
#     file.write(str(id) + ",")
#     if option:
#         for r in result:
#             file.write(str(r[0]) + ":" + str(r[1]) + ",")
#     else :
#         for r in result:
#             file.write(str(r[0])+",")
#     file.write("\n")
#
# #
#
# def run(model,feature_names):
#     file = open(file_, 'w')
#     with open(file_path) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#
#             file.write(str(row['newsId']) + ",")
#             id= str(row['newsId'])
#             content, title, link, tags, content_PoS = get_content_id(id)
#             tag_postag = []
#             if (tags != None) :
#                 tag_postag = check_tag_postag(tags, content)
#
#             result = []
#             keys = run_rake(stoppath, content, content_PoS)
#             # print("key", keys)
#             # tf_idf = get_tfidf_(id, model, feature_names)
#             # print("keys:", keys)
#             # for i in range(len(keys)):
#             #     w = keys.__getitem__(i)
#                 # print(w)
#                 # for j in range(len(tf_idf)):
#                 #     sub = tf_idf[j].split(":")
#                 #     if w[0] == sub[0]:
#                         # print(sub[1])
#                         # result.append((w[0], float(w[1]) * float(sub[1])))
#                 # print("\n")
#             result.sort(key=lambda x: x[1], reverse=True)
#             result = check_keyword(result, content_PoS)
#             check = [tg for tg in tag_postag if tg not in result]
#             # print("check", check)
#             result = result + check
#             file.write(str(result[:]))
#             file.write("\n")
#             # print("result ", result)



#######################################################################


def get_content_id(aid):

    row = get_token(aid)
    title = str(row['title_token']).lower()
    link = get_news(aid)['url']
    content = title + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()
    tag = row["tag_postag"]
    tag_token   = row['tag_token'].lower()
    content_PoS = str(row['title_postag'])+" "+str(row['sapo_postag'])+" "+str(row['content_postag'])
    print("title postag :", row["title_postag"])


    return content,title,link,tag,tag_token,content_PoS


def get_tfidf_(aid, model,feature_names) :
    word_tfidf = []
    tfidf = get_tf_idf(aid, model,feature_names)
    for d in tfidf:
        word_tfidf.append(str(d[0]) + ":" + str(d[1]))

    return word_tfidf


# check tag in the content of news
def check_tag_postag(tags,tag_token, content):
    check = ['Np', 'Nb']
    # print("tags",tags)
    tag_pos = tags.split(" ")

    # print("tag_token",tag_token)
    tokenizer_tag = tag_token.split(";")
    # print("tokenizer_tag",tokenizer_tag)
    # print(tag_pos)
    tokens = word_tokenize(content)
    result = []

    for t in tag_pos:
        w = ''
        postag = ''
        for i in range(len(t)):
            if t[-i] == "/":
                w = t[-len(t):-i].lower()
                postag = t[-i + 1:]
                break
        if (postag in check and w in tokens and w not in result ):
            for tokenizer in tokenizer_tag :
                token = tokenizer.split(" ")
                if w in token and tokenizer not in result :
                    result.append(tokenizer)
                    break
    # print("tag",result)
    return  result


#check PoS of keyword
def check_keyword(result,content_PoS):
    pos = ["V"]
    data_pos = load_postag(content_PoS)
    print("data_pos",data_pos)
    tag = []
    for r in result :
        tag.append(r[0])
    print("keyword ", tag)

    for re in tag :
        # print(re.split(" "))
        if(len(re.split(" ")) == 1) :
            print(re)



    if len(result) >= threshold :
        thr = threshold
    else: thr = len(result)
    tag = tag[:thr]


    return tag


def run_api(id,model,feature_names) :
    content, title, link,tags,tag_token,content_PoS = get_content_id(id)
    tag_postag = []
    if (tags != None):
        tag_postag = check_tag_postag(tags,tag_token, content)
    result= []
    keys = run_rake(stoppath, content,content_PoS)
    tf_idf = get_tfidf_(id, model, feature_names)
    print("keys:", keys)
    for i in range(len(keys)):
        w = keys.__getitem__(i)
        print(w)
        for j in range(len(tf_idf)):
            sub = tf_idf[j].split(":")
            if w[0] == sub[0]:
                print(sub[1])
                result.append((w[0], float(w[1]) * float(sub[1])))
        print("\n")
    result.sort(key=lambda x: x[1], reverse=True)

    result = check_keyword(result, content_PoS)
    check = [tg for tg in tag_postag if tg not in result]
    print("check", check)
    result = result + check
    print("result ", result)

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
    model,feature_names = load_model()
    id = "20180802155615178"
    # content, title, link,tags,tag_token,content_PoS = get_content_id(id)
    # check_tag_postag(tags,tag_token,content)
    run_api(id,model,feature_names)
    # run(model,feature_names)
    # check_keyword(id,[])

    print("--- %s seconds ---" % (time.time() - start))


