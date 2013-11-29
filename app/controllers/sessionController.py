from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from functools import wraps
from datetime import datetime
import time
from werkzeug._internal import _log

from app import app
from app import db

from app.models.user import User
from app.models.session import UserSession
from app.models.course import Course

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

@app.route('/session/create' , methods = ['POST' , 'GET'])
@endSession_required
@login_required
def create():
    user = User.getUserFromSession()
    #sessionName = request.form['sessionName']
    sessionName = "test"
    course = Course.querry.filter_by(id=request.form['course_ID'])
    session1 = UserSession(sessionName, user, course )    
    db.session.add(session1)
    db.session.commit()  
    session['sessionID'] = session1.id
    session['isPauzed'] = None     
    return "sessie aangemaakt"
  
@app.route('/session/start')
@session_required
@login_required
def startSession():
    UserSession.query.filter_by(id=session['sessionID']).first().start()
    return "sessie gestart"

@app.route('/session/pause')
@session_required
@login_required
def pauseSession():
    u = User.query.get(session['userID'])
    _log("info", u.__str__())
    s = u.getRunningSession()
    s.startPause()
    
    return "gepauzeerd"

@app.route('/session/resume')
@session_required
@login_required
def resumeSession():
    s = User.query.get(session['userID']).getRunningSession()
    s.endPause()
    
    return "resume"

@app.route('/session/isPaused')
def isPauzed():
    u = User.query.get(session['userID'])
    s = u.getRunningSession()
    
    if s:
        return s.isPaused().__repr__()
    else:
        return "No running sessions" 

@app.route('/session/end')
@session_required
@login_required
def endSession():
    sessionID = session['sessionID']
    UserSession.query.filter_by(id=session['sessionID']).first().end()
    session.pop('sessionID',None)
    session.pop('isPauzed',None)
    return json.dumps(sessionID)

@app.route('/session/postFeedback' , methods = ['GET' , 'POST'])
@login_required
def postFeedback():
    sessionID = request.form['sessionID']
    UserSession.query.filter_by(id=session['sessionID']).first().setFeedback()
    return render_template('pages/dashboard.html')

@app.route('/session/commit', methods = ['GET' , 'POST'])    
@login_required
@endSession_required
def commitSession():
    "calc and save's the session avarge's"
    sessionID = request.form['sessionID']
    UserSession.query.filter_by(id=session['sessionID']).first().commitSession()
    return render_template('pages/dashboard.html')
