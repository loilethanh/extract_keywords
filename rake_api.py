from flask import Flask, jsonify
from rake_run import *
from src.tfidf import *
from cosine_similar import *

application = Flask(__name__)

file_model = 'models/vectorizer.pk'
stoppath="data/stoplists/vietnamese-stopwords.txt"

models,feature_names = load_model(file_model)
stop_words = load_stopwords_tfidf(stoppath)

candidate_news = get_tags_limit_day()
candidate_news_tfidf,list_contents = get_all_tfidf(models,candidate_news)



@application.route("/<id>")

def get_tag(id):
    result , contents = run_api(id,stop_words,models,feature_names)
    title = contents['title']
    link=contents['link']
    # print(result, title, link)
    return jsonify({'id':id,'title':title, 'link':link, 'keyword': result})

@application.route("/new/<id>")

def getnew(id):
    news = get_news_similar_score(id,stop_words, models, feature_names,candidate_news,candidate_news_tfidf,list_contents)
    # print("news", news)
    return jsonify(news)


if __name__ == "__main__":

    application.run(host="0.0.0.0", port=9001)