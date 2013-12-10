from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from userController import login_required

from app import app
from app import db

from app.models.course import Course
from app.models.user import User

from werkzeug._internal import _log
from werkzeug import secure_filename

@app.route('/course/getAllFollowers')
def getAllFollowers():
    course = Course.query.filter_by(id=request.form['courseID']).first()
    return course.getAllUsers().__str__()

@app.route('/course/followCourse' , methods=['GET', 'POST'])
def followCourse():
    error = None
    user = User.query.filter_by(id=session['userID']).first()
    course = Course.query.filter_by(id=request.form['courseID']).first()
    if(user in course.getAllUsers()):
        error = "User already follows course"
    else:
        course.addUserToCourse(user)
    return error

@app.route('/course/unFollowCourse' , methods=['GET', 'POST'])
def unfollowCourse():
    error = None
    user = User.query.filter_by(id=session['userID']).first()
    course = Course.query.filter_by(id=request.form['courseID']).first()
    if not(user in course.getAllUsers()):
        error = "User doesn't follow this course"
    else:
        course.deleteUser(user)
    return error

@app.route('/course/getAllCourses')
def getAllCourses():
    return Course.getAllCourses()

