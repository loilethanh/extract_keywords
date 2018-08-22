from __future__ import absolute_import
from __future__ import print_function
from src.rake import *
from src.tfidf import *
import csv
from src.data_access import *
import time
from setup import *
import datetime


def run_rake(text,content,min_freq) :
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
        keywords = rake_object.run(text = text,content_pos= content,pos = pos)
    except Exception as e:
        print(e)
        keywords = rake_object.run(text = text,content_pos= content,pos = pos1)

    return keywords

#########################################################################
def run_all_data(stop_words,model, feature_name):

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
            print("id ------------------------",id)
            publish_date = row['update_time']
            update_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            result,contents = run_api(id,stop_words,model,feature_name)
            string = ''
            for r in result :
                string +=r+";"

            print(id,update_date,publish_date,string)
            insert(id,update_date,publish_date,string)
            file.write(id+":"+string)
            file.write("\n")
    file.close()


def get_content(aid):
    """
    get content, title, link, tag from MYSQL with aid
    :param aid:
    :return:
    """
    # start = time.time()

    result ={}
    row = get_new(aid)
    title = row['title_token'].lower()
    # print("title",title)
    link = row['url']
    content = row['sapo_token'].lower() + " " + row['content_token'].lower()
    tag_pos = row["tag_postag"]
    tag_token = ""
    if row['tag_token'] !=None :
        tag_token   = row['tag_token'].lower()
    content_PoS = str(row['title_postag'])+" "+str(row['sapo_postag'])+\
                  " "+str(row['content_postag'])
    result.update({"title":title,"link":link,"content":content,
                   "tag_pos":tag_pos,"tag_token":tag_token,"content_PoS":content_PoS})

    # print("time get content %s ", time.time() - start)
    return result


def get_tfidf_(stop_words,contents, model,feature_names) :
    # start = time.time()
    word_tfidf = []
    tfidf = get_tf_idf(stop_words ,contents, model,feature_names)
    for d in tfidf :
        word_tfidf.append(str(d[0]) + ":" + str(d[1]))
    # print("time get tfidf %s ", time.time() - start)
    return word_tfidf


def check_tag_postag(tag_pos,tag_token, content):
    """ check tag in the content of news """
    # start = time.time()
    check = ['Np']
    # print("tag_news :", tag_pos)
    tags_pos = tag_pos.split(" ")
    tokenizer_tag = tag_token.split(";")
    tokens = word_tokenize(content)
    result = []

    for t in tags_pos:
        w = ''
        postag = ''
        for i in range(len(t)):
            if t[-i] == "/":
                w = t[-len(t):-i].lower().strip()
                postag = t[-i + 1:].strip()
                break
        if (postag in check and w in tokens):
            # print(w,postag)
            for tokenizer in tokenizer_tag:
                token = tokenizer.split(" ")
                if w in token and tokenizer.strip() not in result:
                    result.append(tokenizer.strip())

    # print("tag", result)
    # print("time check tag postag  %s ", time.time() - start)
    return  result


def check_tag(tag_token, content) :
    """
    Check tag of news not in content of the news
    :param tag_token:
    :param content:
    :return: list of tags satisfy exist in the content of news
    """
    # start = time.time()
    tag = tag_token.split(";")
    remove = []
    for tg in tag :
        if tg.replace("_"," ") not in content.replace("_"," ") :
            remove.append(tg)
    result = [tg for tg in tag if tg not in remove]
    # print("check tag" , result)

    # print("time check tag in content %s ", time.time() - start)
    return result


def check_keyword(result,content_PoS):
    """
    Check postag of keyword generated
    """
    # start = time.time()

    # check_pos_word = ['Z','N','Nc','M','R','Nb','V','A']

    data_pos = load_postag(content_PoS)
    # print("data_pos",data_pos)
    tags = []
    tags_remove = []
    for r in result :
        tags.append(r[0].strip())
    # print("keyword_sort ",len(tags) ,tags)

    for i in range(len(tags)) :
        token = tags[i].split(" ")
        if len(token) == 1 and len(token[0].split("_")) == 1 :
            # PoS = data_pos.get(token[0])
            # print(i," ",token," ",PoS)
            #
            # if PoS in check_pos_word :
            #     print("----------remove---------", tags[i], PoS)
            tags_remove.append(token[0])
        else :
            # print(i, " ", token)
            PoS = ''
            for w in token:
                if (data_pos.get(w)):
                    # print(w, data_pos.get(w))
                    PoS += data_pos.get(w)
            # print(tags[i], PoS)
            if (PoS in check_pos):
                # print("----------remove---------", tags[i], PoS)
                tags_remove.append(tags[i])

    tags_final =[tg for tg in tags if tg not in tags_remove]
    # print("remove :",len(tags_remove),"----- keyword :",len(tags_final),tags_final)
    if len(result) >= threshold :
        thr = threshold
    else: thr = len(result)
    tags_final = tags_final[:thr]
    # print("time check keywords %s ", time.time() - start)

    return tags_final



def run_api(id,stop_words,model,feature_names) :
    min_freq = 2
    result = []
    contents = get_content(id)
    cont = contents['title']+" "+contents['content']
    keys = run_rake(cont, contents['content_PoS'],min_freq)
    print("gen_keys_2:",len(keys), keys)

    if len(keys) < 3:
        min_freq = 1
        keys = run_rake(cont, contents['content_PoS'], min_freq)
        print("gen_keys_1:", keys)

    if keys != None :
        tf_idf = get_tfidf_(stop_words,contents, model, feature_names)
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
    if (contents['tag_pos'] != None and contents['tag_token'] != None):
        tag_news = check_tag_postag(contents['tag_pos'],contents['tag_token'], contents['content'])


    result = check_keyword(result, contents['content_PoS'])

    if len(tag_news) == 0 and len(result) < 3 and contents['tag_token'] != None:
        tag_news = check_tag(contents['tag_token'],cont)


    check = [tg for tg in tag_news if tg not in result]

    check_intersect = []
    for re in result :
        for tg in check :
            if re.replace("_", " ") in tg.replace("_", " "):
                check_intersect.append(re)
                break
    print("coincident :",check_intersect)
    result =[re for re in result if re not in check_intersect]
    print("check", check)
    result = check + result
    print("result ", result)

    return  result , contents


def run_content(row,stop_words,model,feature_names) :
    min_freq = 2
    result = []

    contents = {}
    title = row['title_token'].lower()
    link = row['url']
    content = row['sapo_token'].lower() + " " + row['content_token'].lower()
    tag_pos = row["tag_postag"]
    tag_token = ""
    if row['tag_token'] != None:
        tag_token = row['tag_token'].lower()
    content_PoS = str(row['title_postag']) + " " + str(row['sapo_postag']) + " " + str(row['content_postag'])
    contents.update({"title": title, "link": link, "content": content,
                   "tag_pos": tag_pos, "tag_token": tag_token, "content_PoS": content_PoS})


    cont = contents['title']+" "+contents['content']
    keys = run_rake(cont, contents['content_PoS'],min_freq)
    # print("gen_keys_2:",len(keys), keys)

    if len(keys) < 3:
        min_freq = 1
        keys = run_rake(cont, contents['content_PoS'], min_freq)
        # print("gen_keys_1:", keys)

    if keys != None :
        tf_idf = get_tfidf_(stop_words,contents, model, feature_names)
        for i in range(len(keys)):
            w = keys.__getitem__(i)
            # print(w)
            for j in range(len(tf_idf)):
                sub = tf_idf[j].split(":")
                if w[0] == sub[0]:
                    # print(sub[1])
                    result.append((w[0], float(w[1]) * float(sub[1])))
            # print("\n")
        result.sort(key=lambda x: x[1], reverse=True)

    tag_news = []
    if (contents['tag_pos'] != None and contents['tag_token'] != None):
        tag_news = check_tag_postag(contents['tag_pos'],contents['tag_token'], contents['content'])


    result = check_keyword(result, contents['content_PoS'])

    if len(tag_news) == 0 and len(result) < 3 and contents['tag_token'] != None:
        tag_news = check_tag(contents['tag_token'],cont)


    check = [tg for tg in tag_news if tg not in result]

    check_intersect = []
    for re in result :
        for tg in check :
            if re.replace("_", " ") in tg.replace("_", " "):
                check_intersect.append(re)
                break
    # print("coincident :",check_intersect)
    result =[re for re in result if re not in check_intersect]
    # print("check", check)
    result = check + result
    # print("result ", result)

    return  result

# if __name__ == '__main__' :
#
#     model,feature_names = load_model(file_model)
#
#     start = time.time()
#     stop_words = load_stopwords_tfidf(stoppath)
#     print("time load stop words :", time.time() - start )
#     id = "20180814141652967"
#     start = time.time()
#     results , contents = run_api(id,stop_words,model,feature_names)
#     # print("contents :",contents)
#     # run_all_data(stop_words,model,feature_names)
#     print("--- %s seconds ---" % (time.time() - start))
#     # get_content(id)

