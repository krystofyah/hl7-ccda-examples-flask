import configparser
import os
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('app/config.ini')

if os.environ.get("HEROKU"):
    uri = os.environ.get("MONGODB_URI")
    database = os.environ.get("DATABASE_NAME")
    client = MongoClient(uri)
else:
    #database = 'ccdaExamples'
    #client = MongoClient('localhost', 27017)
    database = 'heroku_brpn0kqd'
    client = MongoClient("mongodb://heroku_brpn0kqd:ji373v99tdvndpb3ccpvhg0sqe@ds155091.mlab.com:55091/heroku_brpn0kqd")
db = client[database]
