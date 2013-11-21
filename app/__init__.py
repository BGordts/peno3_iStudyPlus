# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#Initialise the app and its subparts
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'

db = SQLAlchemy(app)

# import the rest of the application
from app.controllers.userController import *
from app.controllers.sessionController import *
from app.controllers.sensorDataController import *

from app.models.user import User

def createTestData():
    db.delete_all()
    db.create_all()
    admin = User('admin@example.com', 'admin', 'admin', 'admin')
    guest = User('b@a.be', 'kaka', 'pipi', 'kaka')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()