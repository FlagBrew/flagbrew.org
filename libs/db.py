from pymongo import MongoClient, uri_parser
import datetime

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


def updateData(mongo, collection, data, downloads):
    if isinstance(data, list):
        update_many(mongo, collection, data, downloads)
    else:
        # update_one(mongo, collection, data)
        print("nah")


# def update_one(mongo, collection, data):
#     mongo[collection].update_one(data)

def update_many(mongo, collection, data, downloads):
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

def get_one(mongo, collection, name):
    return mongo[collection].find_one({"name": name})


def get_all(mongo, collection, field):
    if field == None:
        return mongo[collection].find({})
    else:
        return mongo[collection].find({}, {field: 1})
