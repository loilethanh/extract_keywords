from sklearn.metrics.pairwise import cosine_similarity
from src.rake_run import *
from src.tfidf import *
import time
from setup import *


def get_all_tfidf(models,candidate_news):
    results = {}
    list_id = []
    # for cn in candidate_news :
    #     list_id.append(cn['newsId'])

    # list_contents = get_news_list(list_id)
    # list_contents = ''
    print("lenght of candidate_news : ", len(candidate_news))
    for row in candidate_news :
        title =row['title_token'].lower()
        content = row['sapo_token'].lower() + " " + row['content_token'].lower()
        tfidf = models.transform([title + " " + content])
        results.update({row['news_id']:tfidf})
    return results


def get_news_tags(aid,model,candidate_news,candidate_news_tfidf):
    # tags_news,contents  = run_api(aid,stop_words, model, feature_name)
    start = time.time()
    contents = get_all_content(aid)
    tags = contents['tags'].lower().split(";")[:-1]
    tfidf = model.transform([contents['title_token'].lower()
                             + " " + contents['sapo_token'].lower()
                             + " " + contents['content_token'].lower()])
    print("tags :",tags)
    news=[]
    for i  in range(len(candidate_news)) :
        news_tag = candidate_news[i]['tags'].lower().split(";")[:-1]
        result = {}
        intersect = [t for t in tags if t in news_tag]
        if len(intersect) > 0 and str(aid) != str(candidate_news[i]['news_id']):
            tfidf = candidate_news_tfidf[candidate_news[i]['news_id']]
            result.update({"id": candidate_news[i]['news_id'], "keyword_join": intersect,'tfidf':tfidf,
                           "title":candidate_news[i]['title'],"url":candidate_news[i]['url']})
            news.append(result)
    print("time for get tags of news intersect with id : ", time.time() - start)
    return news,tfidf


def get_news_similar_score(id,model,candidate_news,candidate_news_tfidf):

    news,tfidf = get_news_tags(id,model, candidate_news,candidate_news_tfidf)
    print("lenght of news intersect tags :", len(news))
    start = time.time()
    result = []
    if len(news) != 0:
        # tfidf = model.transform([contents['title_token'].lower()
        #                          +" "+contents['sapo_token'].lower()
        #                          +" "+contents['content_token'].lower()])
        for row in news:
            tf_idf = row['tfidf']
            cosine = cosine_similarity(tfidf, tf_idf)
            result.append((row['id'],cosine[0][0],row['keyword_join'],
                           row['title'], row['url']))
            #
            result.sort(key=lambda x: x[1], reverse=True)
    print("time for get similar score : " , time.time() - start)
    return result




