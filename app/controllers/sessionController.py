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
    u = User.getAdminUser()
    s = Session("testsessie", u)
    s.startSession()
    
    db.session.add(s)
    db.session.commit()    
    
    return "sessie aangemaakt"
  
@app.route('/session/isSessionRunning')  
def isSessionRunning():
    u = User.getAdminUser()
    s = Session.hasRunningSession(u)
    
    _log('info', u.__str__())
    _log('info', s.__str__())
    
    return "Ge hebt runnende sessies" if s else "geen runnende sessies"