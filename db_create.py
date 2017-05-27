#!flask/bin/python
from app.db import db
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

results = db.examples.find()
print results 
