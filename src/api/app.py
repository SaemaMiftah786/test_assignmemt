from flask import Flask, request, jsonify
import pymongo
import pandas as pd
from bson import json_util

app = Flask(__name__)


client = pymongo.MongoClient('localhost', 27017)
db = client.bbc
collecton = db.bbc_news

@app.route('/')
def hello():
    return 'hey lets get some news'

@app.route('/news/<string:keyword>', methods=['GET'])
def get_news(keyword):
    data_cursor = collecton.find({"$text": {"$search": keyword}})
    # for data in data_cursor:
    #     news = data['text']
    df = json_util.dumps(data_cursor, default=json_util.default)
    return jsonify(df)

if __name__ == '__main__':
    app.run(debug=True)