import uuid
from flask import (
    Flask,
    request,
    make_response,
    session,
    redirect,
    url_for,
    jsonify,
    current_app,
    render_template,
    g
)
from app import application

#   blueprints
from search import search
import configparser
import ipdb


config = configparser.ConfigParser()
config.read('app/config.ini')

application = Flask(__name__)
application.config.update(
        SECRET_KEY=config['GENERAL']['SECRET_KEY']
)

from db import db
from bson.objectid import ObjectId

#application.register_blueprint(search)
#search.config=config

@application.route('/', methods=['GET', 'POST'])
@application.route('/sections', methods=['GET', 'POST'])
def get_list_sections_page():
    examples = db.sections.find({})
    #   return render_template("orig.html", examples=examples)
    return render_template("sections.html", examples=examples)


@application.route('/sections/<section_id>', methods=['GET', 'POST'])
def get_section_page(section_id):
    section = db.sections.find_one({"_id": ObjectId(section_id)})
    examples = db.examples.find({"section": section['name']})
    #   return render_template("orig.html", examples=examples)
    return render_template("examples.html", section=section, examples=examples)

@application.route('/examples/view/<permalink_id>', methods=['GET', 'POST'])
def get_example_page(permalink_id):
    example = db.examples.find_one({"Permalink": permalink_id})
    #   return render_template("orig.html", examples=examples)
    return render_template("example.html", example=example)


import configparser

@application.before_request
def before_request():
    print "initialize db"

"""
@application.errorhandler(404)
def not_found(error):
    isAPI=False
    try:
        isAPI=request.path.lower().startswith('/api/')
    except:pass
    if isAPI:
        return make_response(jsonify({'error':'Not found' if error.code==404 else error.description}),error.code)
    return render_template('error.html',error=error),error.code
"""

@application.route("/down")
def down():
    return render_template("down.html")
