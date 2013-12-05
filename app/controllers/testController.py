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
    db.create_all()
    make_courses()
    return "al de data gewist"

@app.route('/test/createTestUsers')
def createTestUsers():
    admin = User('admin@example.com', 'admin', 'admin', 'admin' , "1e Bach Burgerlijk Ingenieur")
    i = 0;
    data = admin.email +'\n'
    while i < 20:
        str = i.__str__()
        testUser = User('test'+str+'@example.com','voornaam'+str,'achternaam'+str,'passwoord',"1e Bach Burgerlijk Ingenieur",'device'+str)
        db.session.add(testUser)
        data = data + testUser.email +'\n'
        i = i+1
    db.session.commit()
    return data

@app.route('/test/recreateAll')
def recreateAll():
    clearDataBase()
    createTestUsers()
    addCourses()
    
    return "done"
 
@app.route('/test/createRandomTestSessions')   
def createTestSessions():
    x = 0
    data = ""
    while x < 50:
        userID = random.randint(1,21)
        user = User.query.get(userID)
        courseID = random.randint(1,11)
        course = Course.query.get(courseID)
        userSession = UserSession(user, course, "Ik ben aan het studeren, dus ik ben een goede student!")
        userSession.start()
        db.session.add(userSession)
        db.session.commit()
        i = 0
        j = random.randint(1,100)
        datafreq = random.uniform(0.0,0.1)
        while not(i==j):
            generateTestData(userSession,datafreq)
            i = i+1
        userSession.end()
        userSession.setFeedback(random.random())
        userSession.commitSession()
        data = data + user.email.__str__() + " heeft een tracked session gedaan voor het vak: " + course.course + ". de data is met een freq " + datafreq.__str__() + " gegenereert en dit is " + j.__str__() + " keer gebeurt. totale studietijd: " + userSession.getSessionDuration().__str__() + " seconden."
        data = data + "\n"
        x = x+1
    return data

def generateTestData(usersession,datafreq):
    time.sleep(datafreq)
    db.session.add(Sensordata("temperature", usersession, random.randint(10,30), datetime.utcnow()))
    db.session.add(Sensordata("humidity", usersession, random.randint(0,100), datetime.utcnow()))
    db.session.add(Sensordata("sound", usersession, random.randint(40,80), datetime.utcnow()))
    db.session.add(Sensordata("illumination", usersession, random.randint(200,900), datetime.utcnow()))
    db.session.add(Sensordata("focus", usersession, bool(random.getrandbits(1)), datetime.utcnow()))
    db.session.commit()

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
        


    
    
