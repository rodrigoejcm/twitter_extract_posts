from pymongo import MongoClient
import json


client = MongoClient()
            
# Use twitterdb database. If it doesn't exist, it will be created.
db = client.twitter

# Decode the JSON from Twitter
with open('/home/rodrigo/Projects/twitter_test_birdy_lib/twitter_ss.json') as json_data:
    datajson = json.load(json_data)


#insert the data into the mongoDB into a collection called twitter_search
#if twitter_search doesn't exist, it will be created.
db.twitter_search.insert(datajson)

for tweet in db.twitter_search.find():
    print(tweet)