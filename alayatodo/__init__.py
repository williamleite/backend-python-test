import os

from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# configuration
from alayatodo.service import messages

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)

DATABASE = os.path.join(app.name, 'tmp', 'alayatodo.db')
DATABASE_ABSOLUTE = os.path.join(app.root_path, 'tmp', 'alayatodo.db')
SQLALCHEMY_DATABASE_URI = r'sqlite:///%s' % DATABASE_ABSOLUTE

app.config.from_object(__name__)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = '%s - %s' % messages.ERROR_LOGINREQUIRED
login_manager.init_app(app)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import alayatodo.service.security
import alayatodo.controller
