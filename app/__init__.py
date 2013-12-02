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
from app.controllers.deviceController import *
from app.controllers.coursController import *
from app.controllers.testController import *
from app.controllers.statisticsController import *

from app.models.user import User
from app.models.userSession import UserSession
from app.models.statistics import Statistics
from app.models.sensordata import Sensordata
from app.models.course import Course
from app.models.courseUsers import Courses_Users
from app.models.device import Device

UPLOAD_FOLDER = '/static/images/profilePics'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def createTestData():
    db.drop_all()
    db.create_all()
    admin = User('admin@example.com', 'admin', 'admin', 'admin')
    guest = User('b@a.be', 'kaka', 'pipi', 'kaka')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()

createTestData()
