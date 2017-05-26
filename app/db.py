import configparser

config = configparser.ConfigParser()
config.read('app/config.ini')

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.ccdaExamples
