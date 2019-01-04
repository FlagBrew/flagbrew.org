from pymongo import MongoClient, uri_parser
import datetime
from bson.objectid import ObjectId
from bson.json_util import loads as bson_loads, dumps as bson_dumps
from json import loads as json_loads, dumps as json_dumps
from flask import jsonify as flask_jsonify

dbobj = None
last_date = ""

def db_conn(uri):
    global dbobj

    client = dbobj or MongoClient(uri, socketKeepAlive=True)

    if not dbobj:
        dbobj = client

    return uri_parser.parse_uri(uri), client


def db(uri):
    uri, client = db_conn(uri)

    return client[uri['database']]


def updateData(mongo, collection, data, downloads, isRepo, isTweets):
    if isinstance(data, list):
        update_many(mongo, collection, data, downloads, isRepo, isTweets)
    else:
        # update_one(mongo, collection, data)
        print("nah")

def update_code(mongo, code, app):
    mongo["download_codes"].replace_one({"app": app}, {"app": app, "code": code}, upsert=True)

def update_one(mongo, collection, data):
     mongo[collection].replace_one({"account": data['account']}, data, upsert=True)

def update_many(mongo, collection, data, downloads, isRepo, isTweets):
    if isRepo:    
        global last_date
        for d in data:
            if downloads:
                try:
                    dls = mongo[collection].find_one({"name": d['name']}, {'downloads': 1})
                    last_date = dls['downloads'][-1]['time']
                    if d['downloads'][0]['time'] != last_date:
                        last_date = d['downloads'][0]['time']
                        tmpList = []
                        for dd in dls['downloads']:
                            tmpList.append(dd)
                        tmpList.append(d['downloads'][0])
                        d['downloads'] = tmpList
                    else:
                        dls['downloads'][-1] = d['downloads'][0]
                        d['downloads'] = dls['downloads']
                except Exception as e:
                    print("if this is the first time, then yeah I expect this to happen")
                    print(e)
            if collection == "members":
                mongo[collection].replace_one({"username": d['username']}, d, upsert=True)
            else:
                mongo[collection].replace_one({"name": d['name']}, d, upsert=True)
    elif not isRepo and isTweets:
        # Delete all the tweets
        mongo[collection].delete_many({})
        # Insert the tweets
        for tweet in data:
            mongo[collection].insert_one(tweet)

def get_one(mongo, collection, name):
    return mongo[collection].find_one({"name": name})

def get_download(mongo, collection, code):
    return mongo[collection].find_one({"code": code})

def get_all(mongo, collection, field):
    if field == None:
        return mongo[collection].find({})
    else:
        return mongo[collection].find({}, {field: 1})

def get_repo_downloads(mongo, collection):
    return bson_dumps(mongo[collection].find({}, {"name": 1, "downloads": 1}))

def json(obj):
    if hasattr(obj, '__class__') and obj.__class__.__name__ == 'Cursor':
        try:
            obj = list(obj)
        except:
            obj = dict(obj)

    if isinstance(obj, list):
        obj = {'data': obj}

    return json_loads(bson_dumps(obj))


def jsonify(obj):
    return flask_jsonify(json(obj))
