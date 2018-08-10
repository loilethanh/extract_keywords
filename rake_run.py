from __future__ import absolute_import
from __future__ import print_function
from nltk.tokenize import word_tokenize
from src.rake import *
from src.tfidf import *
import csv
from src.data_access  import *
import src.rake, time



threshold = 5
file_path = "data/data_news_soha_10000.csv"
stoppath = "data/stoplists/vietnamese-stopwords.txt"
file_rake = 'models/rake_v2.txt'
file_model = 'models/vectorizer.pk'
pos = ['Nu', 'Ny', "C", "Cc", "T", 'X', 'E', 'R', 'Z', 'M','A']
pos1 = ['Nu', 'Ny', "C", "Cc", "T", 'X', 'E','Z','R','A']


def run_rake(stop_path,text,content,min_freq) :
    """
    run alogrithm RAKE with
    :param stop_path:
    :param text:
    :param content:
    :param min_freq:
    :return: keywords
    """
    rake_object = Rake(5,3,min_freq)
    try:
        keywords = rake_object.run(stop_path,text = text,content_pos= content,pos = pos)
    except Exception as e :
        print(e)
        keywords = rake_object.run(stop_path, text=text, content_pos=content,pos = pos1)
    return keywords

#########################################################################
def run_all_data(model, feature_name):
    """
    :param model:
    :param feature_name:
    :return: get keyword for file_path and write in file
    """
    file = open(file_rake, 'w')
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id = row['newsId']
            result,title,link = run_api(id,model,feature_name)
            write_file(id,file,result)


def write_file(id, file, result):
    file.write(str(id) + ",")
    for r in result:
        file.write(str(r)+",")
    file.write("\n")


########################################################################


def get_content(aid):
    """
    get content, title, link, tag from MYSQL with aid
    :param aid:
    :return:
    """
    row = get_token(aid)
    title = str(row['title_token']).lower()
    link = get_news(aid)['url']
    content = title + " " + row['sapo_token'].lower() + " " + row['content_token'].lower()
    tag_pos = row["tag_postag"]
    tag_token   = row['tag_token']
    content_PoS = str(row['title_postag'])+" "+str(row['sapo_postag'])+" "+str(row['content_postag'])
    print(aid, "title postag :", row["title_postag"])


    return content,title,link,tag_pos,tag_token,content_PoS


def get_tfidf_(aid,stoppath, model,feature_names) :
    word_tfidf = []
    tfidf = get_tf_idf(aid, stoppath , model,feature_names)
    for d in tfidf :
        word_tfidf.append(str(d[0]) + ":" + str(d[1]))
    return word_tfidf



def check_tag_postag(tag_pos,tag_token, content):
    """ check tag in the content of news """

    check = ['Np']
    print("tag_news :", tag_pos)
    tags_pos = tag_pos.split(" ")

    print("tag_token",tag_token)
    tokenizer_tag = tag_token.split(";")
    print("tokenizer_tag",tokenizer_tag)
    # print(tag_pos)
    tokens = word_tokenize(content)
    result = []

    for t in tags_pos:
        w = ''
        postag = ''
        for i in range(len(t)):
            if t[-i] == "/":
                w = t[-len(t):-i].lower().strip()
                postag = t[-i + 1:]
                break
        if (postag in check and w in tokens):
            print(w,postag)
            for tokenizer in tokenizer_tag:
                token = tokenizer.split(" ")
                if w in token and tokenizer.strip() not in result:
                    print(tokenizer)
                    result.append(tokenizer.strip())

    print("tag", result)

    return  result


def check_tag(tag_token, content) :
    """
    Check tag of news not in content of the news
    :param tag_token:
    :param content:
    :return: list of tags satisfy exist in the content of news
    """
    tag = tag_token.split(";")
    remove = []
    for tg in tag :
        if tg.replace("_"," ") not in content.replace("_"," ") :
            remove.append(tg)
    result = [tg for tg in tag if tg not in remove]

    return result



def check_keyword(result,content_PoS):
    """
    Check postag of keyword generated
    """

    # pos = ["V",'VV','NVV','NNV','NpVV','NV','NpV','VNV','N','VVb']
    check_pos = ["V",'VV','NV','NpV','VVb','Nb','VA','P','A','AA']
    check_pos_word =['N','M','R','Nb','V','A']
    data_pos = load_postag(content_PoS)
    # print("data_pos",data_pos)
    tags = []
    tags_remove = []
    for r in result :
        tags.append(r[0].strip())
    print("keyword_sort ",len(tags) ,tags)

    for i in range(len(tags)) :
        token = tags[i].split(" ")
        if len(token) == 1 and len(token[0].split("_")) == 1 :
            PoS = data_pos.get(token[0])
            print(i," ",token," ",PoS)

            if PoS in check_pos_word :
                print("----------remove---------", tags[i], PoS)
                tags_remove.append(token[0])
        else :
            print(i, " ", token)
            PoS = ''
            for w in token:
                if (data_pos.get(w)):
                    print(w, data_pos.get(w))
                    PoS += data_pos.get(w)
            print(tags[i], PoS)
            if (PoS in check_pos):
                print("----------remove---------", tags[i], PoS)
                tags_remove.append(tags[i])

    tags_final =[tg for tg in tags if tg not in tags_remove]
    print("remove :",len(tags_remove),"keyword",len(tags_final),tags_final)
    if len(result) >= threshold :
        thr = threshold
    else: thr = len(result)
    tags_final = tags_final[:thr]


    return tags_final


def run_api(id,model,feature_names) :
    # min_freq = 2
    # result = []
    # content, title, link,tags,tag_token,content_PoS = get_content(id)
    #
    # """ Get key from RAKE"""
    # keys = run_rake(stoppath, content, content_PoS,min_freq)
    # print("gen_keys_2:",len(keys), keys)
    # if len(keys) < 3:
    #     min_freq = 1
    #     keys = run_rake(stoppath, content, content_PoS, min_freq)
    #     print("gen_keys_1:", keys)
    # if keys != None :
    #     tf_idf = get_tfidf_(id,stoppath, model, feature_names)
    #     for i in range(len(keys)):
    #         w = keys.__getitem__(i)
    #         print(w)
    #         for j in range(len(tf_idf)):
    #             sub = tf_idf[j].split(":")
    #             if w[0] == sub[0]:
    #                 print(sub[1])
    #                 result.append((w[0], float(w[1]) * float(sub[1])))
    #         print("\n")
    #     result.sort(key=lambda x: x[1], reverse=True)
    #
    # tag_news = []
    # if (tags != None or tag_token != None):
    #     tag_token.lower()
    #     tag_news = check_tag_postag(tags,tag_token, content)
    # if tag_news == None and keys == None:
    #     tag_news = tag_token.lower().split(";")
    #
    #
    # result = check_keyword(result, content_PoS)
    #
    #
    # if len(tag_news) == 0 and len(result) < 3 and tag_token !=None :
    #     tag_news = check_tag(tag_token,content)
    #
    # check = [tg for tg in tag_news if tg not in result]
    # check_coincident = []
    # for re in result:
    #     for tg in check:
    #         if re.replace("_", " ") in tg.replace("_", " "):
    #             check_coincident.append(re)
    #             break
    # print("coincident :", check_coincident)
    # result = [re for re in result if re not in check_coincident]
    # print("check", check)
    # result = check + result
    # print("result ", len(result), result)

    min_freq = 2
    result = []
    content, title, link,tags,tag_token,content_PoS = get_content(id)

    keys = run_rake(stoppath, content, content_PoS,min_freq)
    print("gen_keys_2:",len(keys), keys)
    if len(keys) < 3:
        min_freq = 1
        keys = run_rake(stoppath, content, content_PoS, min_freq)
        print("gen_keys_1:", keys)
    if keys != None :
        tf_idf = get_tfidf_(id,stoppath, model, feature_names)
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

    tag_news = []
    if (tags != None and tag_token != None):
        tag_token = tag_token.lower()
        tag_news = check_tag_postag(tags,tag_token, content)

    # if tag_news == None and keys == None :
    #     tag_news = tag_token.lower().split(";")
    result = check_keyword(result, content_PoS)

    if len(tag_news) == 0 and len(result) < 3 and tag_token != None:
        tag_news = check_tag(tag_token,content)


    check = [tg for tg in tag_news if tg not in result]

    check_coincident = []
    for re in result :
        for tg in check :
            if re.replace("_", " ") in tg.replace("_", " "):
                check_coincident.append(re)
                break
    print("coincident :",check_coincident)
    result =[re for re in result if re not in check_coincident]
    print("check", check)
    result = check + result
    print("result ", result)


    return  result , title, link


if __name__ == '__main__' :
    start = time.time()
    model,feature_names = load_model(file_model)
    id = "20180720095037986"
    # run_api(id,model,feature_names)
    run_all_data(model,feature_names)
    print("--- %s seconds ---" % (time.time() - start))


