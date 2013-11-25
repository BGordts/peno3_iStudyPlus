from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from userController import login_required

from app import app
from app import db
from app.models.course import Course
from werkzeug._internal import _log
from werkzeug import secure_filename


def cours_incl_required(test):
    pass

def userFollowsCours(user,cours):
    pass

@login_required
def followCours():
    pass

@login_required
def unfollowCours():
    pass


