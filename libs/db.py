from pymongo import MongoClient, uri_parser

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


def updateData(mongo, collection, data):
    if isinstance(data, list):
        insert_many(mongo, collection, data)
    else:
        insert_one(mongo, collection, data)


def insert_one(mongo, collection, data):
    mongo[collection].insert_one(data)

def insert_many(mongo, collection, data):
    mongo[collection]