from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db

from app.models.user import User
from app.models.session import Session
from app.models.sensordata import Sensordata
from app.models.userStatitics import Userstatistic

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

 
@app.route('/test/createTestSession1')   
def createTestSessions():
    admin = User.query.filter_by(email='admin@example.com').first()
    session1 = Session("analyse", admin)
    session1.start()
    session['isPauzed'] = None
    db.session.add(session1)
    db.session.commit()
    i=0
    while not(i==2):
        generateTestData(session1)
        i = i+1
    endCreateTestData(session1)
    return "ok"

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
    
    
