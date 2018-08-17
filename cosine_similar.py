from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_run import *
from src.data_access import *
from src.tfidf import *
import time
import datetime


file_model = 'models/vectorizer.pk'
# file = "models/rake_test.txt"
def get_all_tfidf(models,candidate_news):
    results = {}
    list_id = []
    for cn in candidate_news :
        list_id.append(cn['newsId'])

    list_contents = get_news_list(list_id)
    for row in list_contents :
        # result = {}
        title =row['title_token'].lower()
        # link = row['url']
        content = row['sapo_token'].lower() + " " + row['content_token'].lower()
        # tag_pos = row["tag_postag"]
        # tag_token = row['tag_token'].lower()
        # content_PoS = str(row['title_postag']) + " " + str(row['sapo_postag']) + " " + str(row['content_postag'])

        # result.update({"title": title, "link": link, "content": content, "tag_pos": tag_pos, "tag_token": tag_token,
        #                "content_PoS": content_PoS})

        tfidf = models.transform([title+" "+content])
        results.update({row['news_id']:tfidf})

    return results,list_contents

def get_news_tags(aid,stop_words, model, feature_name,candidate_news,candidate_news_tfidf,list_contents):
    tags_news,contents  = run_api(aid,stop_words, model, feature_name)
    news=[]

    # start = time.time()
    for i  in range(len(candidate_news)) :
        news_tag = candidate_news[i]['tags']
        result = {}
        intersect = [t for t in tags_news if t in news_tag]
        if len(intersect) > 0 and str(aid) != str(candidate_news[i]['newsId']):
            tfidf = candidate_news_tfidf[candidate_news[i]['newsId']]
            result.update({"id": candidate_news[i]['newsId'], "keyword_join": intersect,'tfidf':tfidf,
                           "title":list_contents[i]['title'],"url":list_contents[i]['url']})
            news.append(result)
    # print("time get news tag %s ",time.time() - start)
    # print("news" , len(news) )
    return news,contents


def get_news_similar_score(id,stop_words, model, feature_name,candidate_news,candidate_news_tfidf,list_contents):

    # start = time.time()
    news,contents = get_news_tags(id,stop_words, model, feature_name,candidate_news,candidate_news_tfidf,list_contents)
    # print("time get news tag total %s ", time.time() - start)
    result = []

    if len(news) != 0:
        # list_ids = []
        # for n in news:
        #     list_ids.append(n['id'])
        #
        # start = time.time()
        # list_content = get_news_list(list_ids)
        # print("time get list content %s ", time.time() - start)

        tfidf = model.transform([contents['title']+contents['content']])
        # print(tfidf)
        # print("list_content :", list_content)

        for doc in news:
            # content = str(doc['title_token']).lower() + " " + str(doc['sapo_token']).lower() + " " + str(
            #     doc["content_token"]).lower()
            # tf_idf = model.transform([content])
            tf_idf = doc['tfidf']
            # # print(tf_idf)
            cosine = cosine_similarity(tfidf, tf_idf)
            # print(cosine)
            # result.append((doc['news_id'], cosine[0][0], doc['title'], doc['url']))
            result.append((doc['id'],cosine[0][0],doc['keyword_join'], doc['title'], doc['url']))
            #
            result.sort(key=lambda x: x[1], reverse=True)
    # print(result)
    return result

if __name__ == '__main__':

    id = "20180618101927423"
    models, feature_names = load_model(file_model)
    stop_words = load_stopwords_tfidf(stoppath)
    start = time.time()
    candidate_news = get_tags_limit_30day()
    print(len(candidate_news))

    candidate_news_tfidf,list_contents = get_all_tfidf(models,candidate_news)
    print(len(candidate_news_tfidf))

    news, contents = get_news_tags(id,stop_words, models, feature_names,candidate_news,candidate_news_tfidf,list_contents)
    print(news)
    start = time.time()
    get_news_similar_score(id,stop_words, models, feature_names,candidate_news,candidate_news_tfidf,list_contents)
    print("times total :", time.time() - start)



