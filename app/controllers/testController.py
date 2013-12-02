from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db

from app.models.user import User
from app.models.userSession import UserSession
from app.models.course import *
from app.models.sensordata import Sensordata

from datetime import datetime
import time
import random

from werkzeug._internal import _log

@app.route('/test/clearAllData')
def clearDataBase():
    db.drop_all()
    return "al de data gewist"

@app.route('/test/createTestUsers')
def createTestUsers():
    db.create_all()
    admin = User('admin@example.com', 'admin', 'admin', 'admin')
    guest1 = User('test1@example.com', 'test1', 'test1', 'test1')
    guest2 = User('test2@example.com', 'test2', 'test2', 'test2')
    guest3 = User('test3@example.com', 'test3', 'test3', 'test3')
    db.session.add(admin)
    db.session.add(guest1)
    db.session.add(guest2)
    db.session.add(guest3)
    db.session.commit()
    return "4 test users gemaakt, waaronder 1 admin."

@app.route('/test/recreateAll')
def recreateAll():
    clearDataBase()
    createTestUsers()
    addCourses()
    
    return "done"
 
@app.route('/test/createTestSession1')   
def createTestSessions():
    admin = User.query.filter_by(email='admin@example.com').first()
    course = Course.query.filter_by(id=1).first()
    
    session1 = UserSession(admin, course, "test")
    session1.start()
    session['isPauzed'] = None
    db.session.add(session1)
    db.session.commit()
    i=0
    while not(i==2):
        generateTestData(session1)
        i = i+1
    endCreateTestData(session1)
    
    session2 = UserSession(admin, course, "test2")
    session2.start()
    session['isPauzed'] = None
    db.session.add(session2)
    db.session.commit()
    i=0
    while not(i==2):
        generateTestData(session2)
        i = i+1
    endCreateTestData(session2)
    return "ok"

@app.route('/test/addCourses')
def addCourses():
    make_courses()
    i = 1
    while i < len(Course.getAllCourses()):
        course = Course.query.filter_by(id=i).first()
        for u in [1,2,3,4]:
            user =  User.query.filter_by(id=u).first()
            course.addUserToCourse(user)
        i = i + 1
    return "elke user volgt elk vak"

@app.route('/test/untrackedSession')
def createUntrackedSession():
    description = "test untracked session"
    courseID = 1
    course = Course.query.get(7)
    feedback_text = "hopelijk is dit inorde"
    start_date = datetime(2000,1,1,0,00,00)
    end_date =  datetime(2000,1,1,12,00,00)
    user = User.getUserFromSession()
    usession = UserSession(user, course , description, feedback_text, start_date, end_date)
    db.session.add(usession)
    db.session.commit()
    return "ok"

@app.route('/test/modifieSession')
def modifieUntrackedSession():
    uSession = UserSession.query.get(1)
    oldId = uSession.id
    newDescription = uSession.description
    newFeedBack_score = uSession.feedback_score
    newStart_date = uSession.start_date
    newEnd_date = uSession.end_date
    if not(newDescription == "is deze aangepast?"):
        newDescription = "is deze aangepast?"
    if not(newFeedBack_score == "nieuweFeedback"):
        newFeedBack_score = "nieuweFeedback"
    if not(newStart_date == newStart_date):
        newStart_date = newStart_date
    if not(newEnd_date == newEnd_date):
        newEnd_date = newEnd_date
    newSession = UserSession(uSession.user, uSession.course, newDescription, newFeedBack_score, newStart_date, newEnd_date)
    db.session.delete(uSession)
    db.session.commit()
    newSession.id = oldId
    db.session.add(newSession)
    db.session.commit()
    return "ok"

@app.route('/test/deleteUntracked')
def deleteUntracked():
    id = request.args['id']
    s = UserSession.query.get(id)
    s.deleteUntrackedSession()
    return "untracked deleted"
        
def endCreateTestData(userSession):
    userSession.end()
    userSession.setFeedback(random.random())
    userSession.commitSession()

def generateTestData(usersession):
    time.sleep(2)
    db.session.add(Sensordata("temperature", usersession, random.randint(10,30), datetime.utcnow()))
    db.session.add(Sensordata("humidity", usersession, random.randint(0,100), datetime.utcnow()))
    db.session.add(Sensordata("sound", usersession, random.randint(40,80), datetime.utcnow()))
    db.session.add(Sensordata("illumination", usersession, random.randint(200,900), datetime.utcnow()))
    db.session.add(Sensordata("focus", usersession, bool(random.getrandbits(1)), datetime.utcnow()))
    db.session.commit()
    
    
