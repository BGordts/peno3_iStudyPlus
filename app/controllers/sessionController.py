from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from functools import wraps
from datetime import datetime 
from werkzeug._internal import _log

from app import app
from app import db

from app.models.user import User
from app.models.session import Session
from app.controllers.userController import login_required

def session_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'sessionID' in session:
            return test(*args, **kwargs)
        else:
            flash('need to create a session first')
            return redirect(url_for('create'))
    return wrap

def endSession_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if not 'sessionID' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to end session first')
            return redirect(url_for('home'))
    return wrap

@app.route('/session/create')
@endSession_required
@login_required
def create():
    user = User.getUserFromSession()
    #sessionName = request.form['sessionName']
    sessionName = "test"
    session1 = Session(sessionName, user)    
    db.session.add(session1)
    db.session.commit()  
    session['sessionID'] = session1.id
    session['isPauzed'] = None     
    return "sessie aangemaakt"
  
@app.route('/session/start')
@session_required
@login_required
def startSession():
    Session.query.filter_by(id=session['sessionID']).first().start()
    session['isPauzed'] = None
    return "sessie gestart"

@app.route('/session/pauze')
@session_required
@login_required
def pauzeSession():
    session['isPauzed'] = datetime.utcnow()

@app.route('/session/end')
@session_required
@login_required
def endSession():
    Session.query.filter_by(id=session['sessionID']).first().end()
    session.pop('sessionID',None)
    session.pop('isPauzed',None)
    return "sessie beindigt"


