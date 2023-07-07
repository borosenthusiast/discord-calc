import secrets_bot
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import pandas as pd
import io

def dbInsert(serverName, reportingUser, channel, value, reportedDate):
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
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
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
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
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
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

#given all the saved information in a given server and channel, return the highest earning day
def dbHighestDay(serverName, channel):
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
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
                "total": {"$max": "$value"}
            }}
        ])
        for item in agg:
            result += ("For " + item['_id']['serverName'] + ": " + item['_id']['channel'] + ", the date of " + item['_id']['reportedDate'].strftime("%B %d, %Y") \
                  + " has the highest earnings of " + str(item['total']) + " gil.\n")
        return result
    except Exception as e:
        print(e)

#given all the saved information in a given server and channel, return the lowest earning day
def dbLowestDay(serverName, channel):
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
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
                "total": {"$min": "$value"}
            }}
        ])
        for item in agg:
            result += ("For " + item['_id']['serverName'] + ": " + item['_id']['channel'] + ", the date of " + item['_id']['reportedDate'].strftime("%B %d, %Y") \
                  + " has the lowest earnings of " + str(item['total']) + " gil.\n")
        return result
    except Exception as e:
        print(e)

# Calculate which day of the week is the most profitable to open up shop
# TODO: Use average rather than total cost to avoid biases in opening up more or longer in a given day
def dbBestDaysOfWeek(serverName, channel):
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
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
                    "weekday": {"$dayOfWeek": "$reportedDate"}
                },
                "total": {"$avg": "$value"}
            }}
        ])
        for item in agg:
            weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            result += ("For " + item['_id']['serverName'] + ": " + item['_id']['channel'] + ", " \
                      + weekday[item['_id']['weekday'] - 1] + " has average earnings of " + str(item['total']) + " gil.\n")
        return result
    except Exception as e:
        print(e)

#Export data into csv file
def dbExport(serverName, channel):
    uri = f'mongodb+srv://{secrets_bot.MONGO_USER}:{secrets_bot.MONGO_PASSWORD}@restodb.xuue7kr.mongodb.net/?retryWrites=true&w=majority'
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    db = client.MyGamingDB
    col = db.MyGamingDB
    try:
        result = ""
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        agg = col.find({"serverName" : serverName, "channel": channel})
        df = pd.DateFrame(agg)
        csv_data = df.to_csv(index=False)
        # Create a file-like object
        csv_file = io.StringIO(csv_data)
        # Create a Discord attachment object, TODO: Move the discord.File function call to the appropriate function
       # attachment = discord.File(csv_file, filename='data.csv')
        return ""
    except Exception as e:
        print(e)
