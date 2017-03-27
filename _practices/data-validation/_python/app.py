import json

from os import getenv

import pymongo
from flask import Flask, request

app = Flask(__name__)
MONGO_CLIENT = pymongo.MongoClient(getenv("MONGO_HOST", "localhost"))
COLLECTION = MONGO_CLIENT.test.articles


@app.route('/category/', methods=['POST'])
def get_articles_by_category():
    category = request.get_json()['category']
    if category == 'drafts':
        return "[]"

    return json.dumps(list(COLLECTION.find({'category': category}, {'_id': False})))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
