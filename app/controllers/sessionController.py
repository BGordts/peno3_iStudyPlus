from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from functools import wraps
from datetime import datetime
import time
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
    return "sessie gestart"

@app.route('/session/pauze')
@session_required
@login_required
def pauzeSession():
    u = User.query.get(session['userID'])
    _log("info", u.__str__())
    s = u.getRunningSession()
    s.startPauze()
    
    return "gepauzeerd"

@app.route('/session/resume')
@session_required
@login_required
def resumeSession():
    s = User.query.get(session['userID']).getRunningSession()
    s.endPauze()
    
    return "resume"

@app.route('/session/isPauzed')
def isPauzed():
    return User.query.get(session['userID']).getRunningSession().isPauzed()

@app.route('/session/end')
@session_required
@login_required
def endSession():
    sessionID = session['sessionID']
    Session.query.filter_by(id=session['sessionID']).first().end()
    session.pop('sessionID',None)
    session.pop('isPauzed',None)
    return json.dumps(sessionID)

@app.route('/session/postFeedback' , methods = ['GET' , 'POST'])
@login_required
def postFeedback():
    sessionID = request.form['sessionID']
    Session.query.filter_by(id=session['sessionID']).first().setFeedback()
    return render_template('pages/dashboard.html')

@app.route('/session/commit', methods = ['GET' , 'POST'])    
@login_required
@endSession_required
def commitSession():
    "calc and save's the session avarge's"
    sessionID = request.form['sessionID']
    Session.query.filter_by(id=session['sessionID']).first().commitSession()
    return render_template('pages/dashboard.html')
