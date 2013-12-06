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

@app.route('/test/simulateData')
def simulatedataBase():
    clearDataBase()
    data =""
    data = data + createTestUsers()
    data = data + createTestSessions()
    data = data + createUntrackedSession()
    data = data + createTestSessions()
    data = data + createUntrackedSession()
    return data    
    
@app.route('/test/clearAllData')
def clearDataBase():
    db.drop_all()
    db.create_all()
    make_courses()
    return "al de data gewist"

@app.route('/test/createTestUsers')
def createTestUsers():
    admin = User('admin@example.com', 'admin', 'admin', 'admin' , "1e Bach Burgerlijk Ingenieur", "adminDev")
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
 
@app.route('/test/createTestSessions')   
def createTestSessions():
    x = 0
    data = ""
    while x < 5:
        userID = 1
        user = User.query.get(userID)
        courseID = 1
        course = Course.query.get(courseID)
        userSession = UserSession(user, course, "Ik ben aan het studeren, dus ik ben een goede student!")
        randomStart = random.randint(1386264114,1416264114)
        userSession.start_date = datetime.fromtimestamp(randomStart)
        randomEnd = randomStart + 20
        userSession.end_date = datetime.fromtimestamp(randomEnd)
        db.session.add(userSession)
        db.session.commit()
        i = 0
        while (i < (randomEnd-randomStart)):
            pauze = random.randint(0,50)
            if(pauze == 1):
                pauze = json.loads(userSession.pauses)
                pauzeTime=random.uniform(0,userSession.getSessionDuration()/5)
                pauze.append( (i,i+pauzeTime) )
                userSession.pauses = json.dumps(pauze)
            generateTestData(userSession,i)
            i = i+50
        userSession.setFeedback(random.random())
        userSession.commitSession()
        data = data + user.email.__str__() + " heeft een tracked session gedaan voor het vak: " + course.course + ". totale studietijd: " + userSession.getSessionDuration().__str__() + " seconden."
        data = data + "\n"
        x = x+1
    return data

@app.route('/test/createTestSession1')   
def createTestSessions1():
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

def generateTestData(usersession,timestamp):
    t = datetime.fromtimestamp(timestamp)
    db.session.add(Sensordata("temperature", usersession, random.randint(10,30), t))
    db.session.add(Sensordata("humidity", usersession, random.randint(0,100), t))
    db.session.add(Sensordata("sound", usersession, random.randint(40,80), t))
    db.session.add(Sensordata("illumination", usersession, random.randint(200,900), t))
    db.session.add(Sensordata("focus", usersession, bool(random.getrandbits(1)), t))
    db.session.commit()

@app.route('/test/createUntrackedSession')
def createUntrackedSession():
    x=0
    data =""
    while x <2:
        userID = random.randint(1,21)
        user = User.query.get(userID)
        courseID = random.randint(1,11)
        course = Course.query.get(courseID)
        randomStart = random.randint(1386264114,1416264114)
        start_date = datetime.fromtimestamp(randomStart)
        randomEnd = randomStart + random.randint(900,14400)
        end_date = datetime.fromtimestamp(randomEnd)
        feedback_text = "dat was een lastige studeersessie"
        userSession = UserSession(user, course , "een untracked studeersessie", feedback_text, start_date, end_date)
        db.session.add(userSession)
        db.session.commit()
        data = data + user.email.__str__() + " heeft een untracked session gedaan voor het vak: " + course.course + ". totale studietijd: " + userSession.getSessionDuration().__str__() + " seconden."
        data = data + "\n"
        x=x+1 
    return data

@app.route('/test/modifieSession')
def modifieUntrackedSession():
    uSession = UserSession.query.get(1)
    oldId = uSession.id
    newDescription = uSession.description
    newFeedBack_score = uSession.feedback_score
    newStart_date = uSession.start_date
    newEnd_date = uSession.end_date
    if not(newDescription == "description is aangepast"):
        newDescription = "description is aangepast"
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
        


    
    
