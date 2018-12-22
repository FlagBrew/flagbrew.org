from pymongo import MongoClient, uri_parser
import datetime

dbobj = None


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
    for d in data:
        if downloads:
            try:
                dls = mongo[collection].find_one({"name": d['name']}, {'downloads'})
                if dls['downloads'][len(dls['downloads'])-1]['time'] == datetime.date.today().strftime("%m/%d/%Y"):
                    dls['downloads'][len(dls['downloads'])-1]['amount'] = d['downloads'][0]['amount']
                else:
                    dls['downloads'].append(d['downloads'][0])
            except Exception as e:
                print("if this is the first time, then yeah I expect this to happen")
                print(e)
        mongo[collection].replace_one({"name": d['name']}, d, upsert=True)