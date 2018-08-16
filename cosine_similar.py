from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_run import *
from src.data_access import *
from src.tfidf import *
import time
import datetime


file_model = 'models/vectorizer.pk'
# file = "models/rake_test.txt"


def get_news_tags(aid, model, feature_name):
    tags_news, title, link  = run_api(aid, model, feature_name)
    news=[]
    start = time.time()
    candidate_news = get_tags_limit_30day()
    print("time get news date %s ",time.time() - start, len(candidate_news))

    start = time.time()
    for cn  in candidate_news :
        news_tag = cn['tags']
        result = {}
        intersect = [t for t in tags_news if t in news_tag]
        if len(intersect) > 0 and str(aid) != str(cn['newsId']):
            result.update({"id": cn['newsId'], "keyword_join": intersect})
            news.append(result)
    print("time get news tag %s ",time.time() - start)
    print("news" , len(news) )
    return news


def get_news_similar_score(id, model, feature_name):
    start = time.time()
    row = get_token(id)
    content = row['title_token'].lower() + row['sapo_token'].lower() + " " + row['content_token'].lower()
    print("time get content %s ", time.time() - start)
    start = time.time()
    news = get_news_tags(id, model, feature_name)
    print("time get news tag total %s ", time.time() - start)
    result = []

    if len(news) != 0:
        list_ids = []
        for n in news:
            list_ids.append(n['id'])
        start = time.time()
        list_content = get_tags_list(list_ids)
        print("time get list content %s ", time.time() - start)

        tfidf = model.transform([content])

        print("list_content :", list_content)

        for doc in list_content:
            contents = str(doc['title_token']).lower() + " " + str(doc['sapo_token']).lower() + " " + str(
                doc["content_token"]).lower()
            tf_idf = model.transform([contents])
            # # print(tf_idf)
            cosine = cosine_similarity(tfidf, tf_idf)
            print(cosine)
            result.append((doc['news_id'], cosine[0][0], doc['title'], doc['url']))
            # result.append((doc['id'],cosine[0][0],doc['keyword_join']))
            #
            result.sort(key=lambda x: x[1], reverse=True)
    # print(result)
    return result

if __name__ == '__main__':

    id = "20180618101927423"
    models, feature_names = load_model(file_model)
    # news = get_news_tags(id, models,feature_names)
    start = time.time()
    get_news_similar_score(id, models, feature_names)
    print("times total :", time.time() - start)



