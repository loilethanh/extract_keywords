from flask import Flask, jsonify
from rake_vn import *
application = Flask(__name__)



@application.route("/<id>")

def get(id):
    result , title, link = run_api(id)
    print(result, title, link)
    return jsonify({'id':id,'title':title, 'link':link, 'keyword': result})


if __name__ == "__main__":
    application.run()