from sklearn.metrics.pairwise import cosine_similarity
from src.rake_run import *
from src.tfidf import *
import time
from setup import *


def get_all_tfidf(models,candidate_news):
    results = {}
    list_id = []
    for cn in candidate_news :
        list_id.append(cn['newsId'])

    list_contents = get_news_list(list_id)
    for row in list_contents :
        title =row['title_token'].lower()
        content = row['sapo_token'].lower() + " " + row['content_token'].lower()
        tfidf = models.transform([title+" "+content])
        results.update({row['news_id']:tfidf})

    return results,list_contents

def get_news_tags(aid,stop_words, model, feature_name,candidate_news,candidate_news_tfidf,list_contents):
    tags_news,contents  = run_api(aid,stop_words, model, feature_name)
    news=[]
    for i  in range(len(candidate_news)) :
        news_tag = candidate_news[i]['tags']
        result = {}
        intersect = [t for t in tags_news if t in news_tag]
        if len(intersect) > 0 and str(aid) != str(candidate_news[i]['newsId']):
            tfidf = candidate_news_tfidf[candidate_news[i]['newsId']]
            result.update({"id": candidate_news[i]['newsId'], "keyword_join": intersect,'tfidf':tfidf,
                           "title":list_contents[i]['title'],"url":list_contents[i]['url']})
            news.append(result)
    return news,contents


def get_news_similar_score(id,stop_words, model, feature_name,candidate_news,candidate_news_tfidf,list_contents):

    news,contents = get_news_tags(id,stop_words, model, feature_name,candidate_news,candidate_news_tfidf,list_contents)
    result = []

    if len(news) != 0:

        tfidf = model.transform([contents['title']+contents['content']])
        for doc in news:
            tf_idf = doc['tfidf']
            cosine = cosine_similarity(tfidf, tf_idf)
            result.append((doc['id'],cosine[0][0],doc['keyword_join'], doc['title'], doc['url']))
            #
            result.sort(key=lambda x: x[1], reverse=True)
    return result




