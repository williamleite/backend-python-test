from flask import Flask, g
import sqlite3
from flask_sqlalchemy import SQLAlchemy

# configuration
DATABASE = '.\\tmp\\alayatodo.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Projects\\backend-python-test\\tmp\\alayatodo.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import alayatodo.views
