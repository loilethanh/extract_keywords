from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_run import *
from src.data_access import *
from src.tfidf import *


file_model = 'models/vectorizer.pk'

def get_news_tags(aid, model, feature_name):
    tags_news, title, link  = run_api(aid, model, feature_name)
    print("tags :",tags_news)
    news=[]
    with open(file_rake) as fp:
        for row in range(0,1000) :
            line = fp.readline().split(",")
            news_tag = line[1:]
            result = {}
            coincident = [t for t in tags_news if t in news_tag]
            if len(coincident)>0 and str(aid) != str(line[0]):
            #     # print(news_ids[row], ":", join)
                titles = get_news(line[0])['title']
                links = get_news(line[0])['url']
                result.update({"id": line[0],"title":titles,"link": links,"keyword_join" : coincident})
            #     result.update({"id": line[0],"keyword" : join})
                print(result)
                news.append(result)
    return news



def get_news_similar_score(id, model, feature_name):
    news = get_news_tags(id, model, feature_name)
    row = get_token(id)
    content = row['title_token'].lower() + row['sapo_token'].lower() + " " + row['content_token'].lower()
    tfidf = model.transform([content])
    # print(tfidf)
    result = []
    for doc in news :
        row = get_token(doc['id'])
        content = row['title_token'].lower() + row['sapo_token'].lower() + " " + row['content_token'].lower()
        tf_idf = model.transform([content])
        # print(tf_idf)
        cosine = cosine_similarity(tfidf,tf_idf)
        # print(cosine)
        result.append((doc['id'],cosine[0][0],doc['title'],doc['link'],doc['keyword_join']))
        result.sort(key=lambda x: x[1], reverse=True)

    print(result)
    return result

if __name__ == '__main__':

    id = "20180720072721908"
    models, feature_names = load_model(file_model)
    # # news = get_new(id, models,feature_names)
    get_news_similar_score(id, models, feature_names)



