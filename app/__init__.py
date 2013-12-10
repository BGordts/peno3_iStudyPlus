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
from app.controllers.baseController import *

from app.models.user import User
from app.models.userSession import UserSession
from app.models.statistics import Statistics
from app.models.sensordata import Sensordata
from app.models.course import Course
from app.models.courseUsers import Courses_Users
from app.models.device import Device

from app.models.course import make_courses
db.create_all()
make_courses()
