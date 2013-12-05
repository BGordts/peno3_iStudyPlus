from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

from app import app
from app import db

from app.models.user import User
from app.models.userSession import UserSession
from app.models.course import Course
from werkzeug._internal import _log
from app.controllers.baseController import welcome
from app.models.courseUsers import Courses_Users

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'userID' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first.')
            return redirect(url_for('login'))
    return wrap

def logout_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if not 'userID' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to logout first.')
            return redirect(url_for('home'))
    return wrap

@app.route('/user/login' , methods=['GET','POST'])
@logout_required
def login():
    error = None
    if request.method == 'POST':
        if not isValidLogin(request.form['username'],request.form['password']):
            error = 'invalid username or password, please try again.'
        else:
            session['userID'] = User.query.filter_by(email= request.form['username']).first().id
            return redirect(url_for("welcome"))
    return render_template('pages/login.html' , error = error)

def isValidLogin( username, password):
    user = User.query.filter_by(email=username).first()
    if user == None or (not user.password == password):
        return False
    return True

from app.controllers.sessionController import endSession_required

@app.route('/user/logout')
@endSession_required
def logout():
    session.pop('userID',None)
    return redirect(url_for('login'))

@app.route('/user/tracking')
@login_required
def tracking():
    return render_template('pages/tracking_page.html')

@app.route('/user/register' , methods = ['GET','POST'])
@logout_required
def register():
    errors = {}
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        pic_small = request.form['profile-img_small']
        pic_big = request.form['profile-img_large']
        deviceID = request.form['device-id']
        if not isValidPass(pass1,pass2):
            error = 'The passwords you entered did not match'
            error.update({"password":error})
        if not isValidEmail(email):
            error = 'The email-address you entered is already taken'
            error.update({"email":error})
        if not((errors and True) or False):
            user = User(email, lastname, name, pass1 , pic_small , pic_big)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('pages/register.html' , errors = errors)

def isValidEmail(username):
    user = User.query.filter_by(email=username).first()
    if user == None:
        return True
    return False

def isValidPass(pass1 , pass2):
    return pass1 == pass2

@app.route('/user/settings' , methods = ['GET','POST'])
@login_required
def changeUserinfo():
    if request.method == 'POST':
        user = User.query.get(request.form['userID'])
        errors = {}
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        oldPass = request.form['oldPass']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        deviceID = request.form['device-id']
        pic_small = request.form['profile-img_small']
        pic_big = request.form['profile-img_large']
        if(email == None):
            email = user.email
        if(name == None):
            name = user.surname
        if(lastName == None):
            lastName = user.name
        if(oldPass == None):
            pass1 = user.password
            pass2 = user.password
        if not isValidEmail:
                error = 'The email-address you entered is already taken'
        if not(user.password == oldPass):
            error = 'The old password you entered did not match'
        if not isValidPass(pass1,pass2):
            error = 'The passwords you entered did not match'
            errors = errors + {"password" : error}
        if not((errors and True) or False):
            user.changeSetting( email , lastname , name , pass1)
        return render_template('pages/settings_page.html' , errors = errors)
    else:
        return render_template('pages/settings_page.html')

@app.route('/user/getCoStudents', methods = ['GET'])
def getCoStudents():
    user = User.getUserFromSession()
    
    coStudents = []
    for courseUser1 in user.courses_Users:
        courseUsers = Courses_Users.query.filter_by(course = courseUser1.course).all()
        for nextCourseUser in courseUsers:
            if not(nextCourseUser.user in coStudents):
                coStudents.append(nextCourseUser.user)
    _log("info", "co students: " + coStudents.__str__())
    return json.dumps([cu.output() for cu in coStudents])

@app.route('/user/courses')
def getUserCourses():
    userID = request.args['userID']
    
    returndict = {}
    
    userCourses = Courses_Users.query.filter_by(user_id=userID).all()
    
    for nextUserCourse in userCourses:
        returndict[nextUserCourse.course_id] = {"name":nextUserCourse.course.course}   
    
    return json.dumps(returndict)

@app.route('/user/getDetailedCourses')
def getDetailedUserCourses():
    userID = request.args['userID']
    
    returndict = []
    
    userCourses = Courses_Users.query.filter_by(user_id=userID).all()
    
    for nextUserCourse in userCourses:
        returndict.append({"id":nextUserCourse.course_id, "name":nextUserCourse.course.course, "statistics":nextUserCourse.courseStatistics.outputData()})
    
    return json.dumps(returndict)

@app.route('/user/getUser')
def getUser():
    userID = request.args['userID']
    
    return json.dumps(User.query.get(userID).output())

@app.route('/user/getCurrentUser')
def getCurrentUser():    
    return json.dumps(User.getUserFromSession().output())