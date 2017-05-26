import configparser
import os
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('app/config.ini')

if os.environ.get("HEROKU"):
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri)
else:
    client = MongoClient('localhost', 27017)

db = client.ccdaExamples
