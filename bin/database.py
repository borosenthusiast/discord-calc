import secrets
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
            "value": str(value),
            "reportedDate": str(reportedDate)
        }
        col.insert_one(earningsDoc)
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
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)