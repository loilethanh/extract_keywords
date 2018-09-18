from flask import Flask, jsonify
from src.cosine_similar import *
from  setup import *
application = Flask(__name__)



models,feature_names = load_model(file_model)
stop_words = load_stopwords_tfidf(stoppath)


candidate_news = get_tags_limit_day()
candidate_news_tfidf = get_all_tfidf(models,candidate_news)



@application.route("/<id>")

def get_tag(id):
    # result,contents = run_api(id,stop_words,models,feature_names)
    start = time.time()
    result = get_all_content(id)
    # title = str(result['title'])
    # link= result['url']
    # tag = result['tags'].split(";")[:-1]
    print("time for get tags : ", time.time() - start)
    return jsonify({'id':id,'title':result['title'],
                    'link':result['url'],
                    'keyword': result['tags'].split(";")[:-1],
                    "time ":time.time() - start })

@application.route("/new/<id>")

def getnew(id):
    start = time.time()
    news = get_news_similar_score(id, models,candidate_news,candidate_news_tfidf)
    print("time for get all news : ", time.time() - start)
    return jsonify({"news" :news,"lenght":len(news),"time ": time.time() - start })


if __name__ == "__main__":

    application.run(host="0.0.0.0", port=9001)