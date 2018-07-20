from flask import Flask, jsonify
from rake_vn import *
application = Flask(__name__)



@application.route("/<id>")

def get(id):
    result , title, link = run_api(id)
    print(result, title, link)
    return jsonify({'id':id,'title':title, 'link':link, 'keyword': result})

@application.route("/new/<id>")

def getnew(id):
    news = get_new(id)
    return jsonify(news)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=9001)