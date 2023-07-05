import secrets
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

def dbInsert(serverName, reportingUser, channel, value, reportedDate):
    uri = f'mongodb+srv://{secrets.MONGO_USER}:{secrets.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    db = client.MyGamingDB
    col = db.MyGamingDB

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        earningsDoc = {
            "serverName": str(serverName),
            "reportingUser": str(reportingUser),
            "channel": str(channel),
            "value": int(value),
            "reportedDate": reportedDate
        }
        col.insert_one(earningsDoc)
    except Exception as e:
        print(e)

def dbTotalByDay(serverName, channel):
    uri = f'mongodb+srv://{secrets.MONGO_USER}:{secrets.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    db = client.MyGamingDB
    col = db.MyGamingDB
    
    try:
        result = ""
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        agg = col.aggregate([
            {"$match": {
                "serverName": serverName,
                "channel": channel
            }},
            {"$group": {
                "_id": {
                    "serverName": "$serverName",
                    "channel": "$channel",
                    "reportedDate": "$reportedDate"
                },
                "total": {"$sum": "$value"}
            }},
            { "$sort" : { "_id" : 1 } }
        ])
        for item in agg:
            result += ("For " + item['_id']['serverName'] + ": " + item['_id']['channel'] + ", on the date of " + item['_id']['reportedDate'].strftime("%B %d, %Y") \
                  + " has total earnings of " + str(item['total']) + " gil.\n")
        return result
    except Exception as e:
        print(e)

def dbTotal(serverName, channel):
    uri = f'mongodb+srv://{secrets.MONGO_USER}:{secrets.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    db = client.MyGamingDB
    col = db.MyGamingDB
    
    try:
        result = ""
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        agg = col.aggregate([
            {"$match": {
                "serverName": serverName,
                "channel": channel
                }
            },
            {"$group": {
            "_id": {
                "serverName" : "$serverName", "channel": "$channel"
                },
            "total" : {"$sum" : "$value"}}}])

        for item in agg:
            result += ("For " + item['_id']['serverName'] + ": " + item['_id']['channel'] \
                  + " has total earnings of " + str(item['total']) + " gil.\n")
        return result
    except Exception as e:
        print(e)