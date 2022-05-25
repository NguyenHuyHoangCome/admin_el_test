from flask import Flask
from os import path
import os
import datetime
from pydoc import Doc
import random
from unicodedata import category
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import *
from collections import OrderedDict
from flask.json import JSONEncoder
from flask_cors import CORS
import pyrebase
import json

link = os.getcwd()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'baconcho'
    CORS(app)
    app.jinja_env.variable_start_string = '{['
    app.jinja_env.variable_end_string = ']}'

    cred = credentials.Certificate(link +"/website/keyfirebase.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'eng-ver-2.appspot.com'})
    # firebase_admin.initialize_app(cred) 
    pb = pyrebase.initialize_app(json.load(open('website/keypb.json')))

    db = firestore.client()
    from .views import views
    from .api import api
    from .auth import auth1
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')
    app.register_blueprint(auth1, url_prefix='/')

    return app
