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

from app.controllers.filters import login_required
from app.controllers.filters import logout_required
from app.controllers.filters import session_required
from app.controllers.filters import endSession_required
from app.models.device import Device

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

#from app.controllers.sessionController import endSession_required

@app.route('/user/logout')
@endSession_required
def logout():
    session.pop('userID',None)
    return redirect(url_for('login'))

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
        deviceID = request.form['deviceID']
        study = request.form['study']
        if not isValidPass(pass1,pass2):
            error = 'The passwords you entered did not match'
            errors.update({"password":error})
        if not isValidEmail(email):
            error = 'The email-address you entered is already taken'
            errors.update({"email":error})
        if not((errors and True) or False):
            user = User(email, lastname, name, pass1 , study, deviceID, pic_small , pic_big)
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
@endSession_required
def changeUserinfo():
    user = User.getUserFromSession()
    device = Device.query.filter_by(user=user).first()
    error = None
    
    if request.method == 'POST':
        errors = {}
        name = request.form['name']
        lastname = request.form['lastname']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']
        deviceID = request.form['deviceID']
        study = request.form['study']
        pic_small = request.form['profile-img_small']
        pic_big = request.form['profile-img_large']
        email = user.email #You can't change your email!
        if(name == ""):
            name = user.surname
        if(lastname == ""):
            lastname = user.name
        if(pass1 == ""):
            pass1 = user.password
            pass2 = user.password
        if(deviceID == ""):
            deviceID = Device.query.filter_by(user=user).first().key
        if(pic_small == ""):
            pic_small = user.picSmall
            pic_big = user.picBig
        if not isValidEmail:
                error = 'The email-address you entered is already taken'
        if not isValidPass(pass1,pass2):
            error = 'De passwoorden waren niet gelijk'
            
        #Serieus Sam? :) if not((errors and True) or False)
        if error:
            _log("info", "kaka error" + error.__str__())
            
            return render_template('pages/settings_page.html' , error = error, user=user, device=device)
        else:
            _log("info", "kaka geen error")
            user.changeSetting( email , lastname , name , pass1,study,deviceID,pic_small,pic_big)   
            
            return redirect("app/" + user.id.__str__() + "/dashboard")
       
    else:
        return render_template('pages/settings_page.html', user = user, device=device)

@app.route('/user/getCoStudents', methods = ['GET'])
def getCoStudents():
    user = User.getUserFromSession()
    
    coStudents = []
    for courseUser1 in user.courses_Users:
        courseUsers = Courses_Users.query.filter_by(course = courseUser1.course).all()
        for nextCourseUser in courseUsers:
            if not(nextCourseUser.user in coStudents):
                coStudents.append(nextCourseUser.user)
    coStudents.remove(user)
    _log("info", "co students: " + coStudents.__str__())
    return json.dumps([cu.outputSmall() for cu in coStudents])

@app.route('/user/courses')
def getUserCourses():
    userID = request.args['userID']
    
    returndict = []
    
    userCourses = Courses_Users.query.filter_by(user_id=userID).all()
    
    for nextUserCourse in userCourses:
        returndict.append({"id":nextUserCourse.course_id, "name":nextUserCourse.course.course})
    
    return json.dumps(returndict)

@app.route('/user/getDetailedCourses')
def getDetailedUserCourses():
    userID1 = request.args['userID1']
    userID2 = request.args['userID2']
    
    returndict = []
    
    userCourses1 = Courses_Users.query.filter_by(user_id=userID1).order_by(Courses_Users.course_id.desc()).all()
    userCourses2 = Courses_Users.query.filter_by(user_id=userID2).order_by(Courses_Users.course_id.desc()).all()
    
    for i in range(0, len(userCourses1)):
        nextUserCourse1 = userCourses1[i]
        nextUserCourse2 = userCourses2[i]
        
        interdict = {}
        interdict["user1"] = {"id":nextUserCourse1.course_id, "name":nextUserCourse1.course.course, "statistics":nextUserCourse1.courseStatistics.outputData()}
        interdict["user2"] = {"id":nextUserCourse2.course_id, "name":nextUserCourse2.course.course, "statistics":nextUserCourse2.courseStatistics.outputData()}
        
        returndict.append(interdict)
    
    return json.dumps(returndict)

@app.route('/user/getUser')
def getUser():
    userID = request.args['userID']
    
    return json.dumps(User.query.get(userID).outputLarge())

@app.route('/user/getCurrentUser')
def getCurrentUser():    
    return json.dumps(User.getUserFromSession().outputLarge())
