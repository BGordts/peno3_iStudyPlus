'''
Created on 7-nov.-2013

@author: Boris
'''
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug._internal import _log

from app import app
from app import db
from app.models.user import User
from app.models.session import Session

@app.route('/session/create')
def create():
    user = User.getAdminUser()
    session = Session("testsessie", user)
    session.startSession()
    
    db.session.add(session)
    db.session.commit()    
    
    return "sessie aangemaakt"
  
def startSession
@app.route('/session/isSessionRunning')  
def isSessionRunning():
    user = User.getAdminUser()
    sensor = Session.hasRunningSession(user)
    
    _log('info', user.__str__())
    _log('info', sensor.__str__())
    
    return "Ge hebt runnende sessies" if sensor else "geen runnende sessies"

