from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug._internal import _log

from app import app
from app import db
from app.models.user import User
from app.models.session import Session
from functools import wraps
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
            return redirect(url_for('create'))
    return wrap


@app.route('/session/create')
@login_required
@endSession_required
def create():
    user = User.getUserFromSession()
    #sessionName = request.form['sessionName']
    sessionName = "test"
    session1 = Session(sessionName, user)    
    db.session.add(session1)
    db.session.commit()  
    session['sessionID'] = session1.id
    session['isPauzed'] = True     
    return "sessie aangemaakt"
  
@app.route('/session/start')
@session_required
@login_required
def startSession():
    _log('info',Session.query.filter_by(id=session['sessionID']).first().__str__())
    Session.query.filter_by(id=session['sessionID']).first().start()
    return "sessie gestart"

@app.route('/session/pauze')
@session_required
@login_required
def pauzeSession():
    session['isPauzed'] = True

@app.route('/session/end')
@session_required
@login_required
def endSession():
    Session.query.filter_by(id=session['sessionID']).first().end()
    session.pop('sessionID',None)
    return "sessie beindigt"


