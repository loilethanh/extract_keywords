from flask import Flask, jsonify
from rake_run import *
from src.tfidf import *
from cosine_similar import *
application = Flask(__name__)

file_model = 'models/vectorizer.pk'


@application.route("/<id>")

def get_tag(id):
    result , title, link = run_api(id,models,feature_names)
    print(result, title, link)
    return jsonify({'id':id,'title':title, 'link':link, 'keyword': result})

@application.route("/new/<id>")

def getnew(id):
    news = get_news_similar_score(id, models, feature_names)
    print("news", news)
    return jsonify(news)


if __name__ == "__main__":
    models,feature_names = load_model(file_model)
    application.run(host="0.0.0.0", port=9001)