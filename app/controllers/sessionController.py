from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from functools import wraps
from datetime import datetime
import time
from werkzeug._internal import _log
import json
from app.utils.utils import *

import time
from app import app
from app import db

from app.models.user import User
from app.models.userSession import UserSession
from app.models.course import Course

from app.models.sensordata import *
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

@app.route('/session/createTracked' , methods = ['GET'])
@endSession_required
@login_required
def createTracked():
    sessionName = request.args["sessionName"]
    courseID = request.args["courseID"]
    
    user = User.getUserFromSession()
    
    #sessionName = request.form['sessionName']
    course = Course.query.get(courseID)
    _log('info', 'lecourse: ' +  course.__str__())
    session1 = UserSession(user, course, sessionName)    
    db.session.add(session1)
    db.session.commit()  
    session['sessionID'] = session1.id
    session['isPauzed'] = None     
    return "sessie aangemaakt"

@app.route('/session/createUntracked' , methods = ['GET'])
@endSession_required
@login_required
def createUntracked():
    description = request.args["sessionName"]
    courseID = request.args["courseID"]
    course=Course.query.get(courseID)
    feedback_text = request.args["feedback"]
    start_date = datetime.fromtimestamp(request.args["start_time"])
    end_date = datetime.fromtimestamp(request.args["start_time"])
    user = User.getUserFromSession()
    usession = UserSession(user, course , description, feedback_text, start_date, end_date)
    db.session.add(usession)
    db.session.commit()
    return "ok"
    
@app.route('/session/modifieSession' , methods = ['POST' , 'GET'])
@login_required
@endSession_required
def modifieUSession():
    uSession = Session.query.get(request.args['sessionID'])
    newDescription = uSession.description
    newFeedBack_score = uSession.feedback_score
    newStart_date = uSession.start_date
    newEnd_date = uSession.end_date
    if not(newDescription == request.args['description']):
        newDescription = request.args['description']
    if not(newFeedBack_score == request.args['feedback']):
        newFeedBack_score = request.args['feedback']
    if not(newStart_date == datetime.fromtimestamp(request.args['startDate'])):
        newStart_date = datetime.fromtimestamp(request.args['startDate'])
    if not(newEnd_date == datetime.fromtimestamp(request.args['endDate'])):
        newEnd_date = datetime.fromtimestamp(request.args['endDate'])
    newSession = UserSession(uSession.user, uSession.course, newDescription, newFeedBack_score, newStart_date, newEnd_date)
    oldId =uSession.id
    db.session.delete(uSession)
    db.session.commit()
    newSession.id = oldId
    db.session.add(newSession)
    db.session.commit()

@app.route('/session/modifieSession' , methods = ['POST' , 'GET'])
@login_required
@endSession_required
def deleteUSession():
    uSession = Session.query.get(request.args['sessionID'])
    uSession.deleteUntrackedSession()       

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
    
    sessionID = session.pop('sessionID',None)
    session.pop('isPauzed',None)
    
    return json.dumps(sessionID)

@app.route('/session/postFeedback' , methods = ['GET'])
@login_required
def postFeedback():
    _log("info", "input= " + request.args['sessionID'])
    _log("info", "input= " + request.args['feedback'])
    sessionID = request.args['sessionID']
    feedback = request.args['feedback']
    
    UserSession.query.get(sessionID).setFeedback(feedback)
    return render_template('pages/dashboard.html')

@app.route('/session/commit', methods = ['GET'])    
@login_required
@endSession_required
def commitSession():
    
    #sessionID = request.form['sessionID']
    userSession = UserSession.query.get(request.args['sessionID'])
    _log("info", "mr usersessio: " + userSession.__str__())
    userSession.commitSession()
    return render_template('pages/dashboard.html')

'''
Get all the sensordata for the spified session and sensor
'''
@app.route('/session/getData', methods = ['GET'])    
@login_required
def getData():
    sessionID = request.args["sessionID"]
    sensor_type = request.args["sensor_type"]
    
    session = Session.query.get(sessionID)
    
    return json.dumps(session.outputSensorData(sensor_type))

'''
Returns all the sessions created by this user
'''
@app.route('/session/getAllSessions', methods = ['GET'])    
@login_required
def getAllSessions():
    user = User.getUserFromSession()
    
    _log("info", user.sessions.all().__str__())
    
    #Move to UserSesssion
    returnList = []
    for lolol in user.sessions.all():
        returnSession = {}
        returnSession['description'] = lolol.description
        returnSession['feedback_text'] = lolol.feedback_text
        returnSession['feedback_score'] = lolol.feedback_score
        returnSession['start_date'] = unix_time_millis(lolol.start_date)
        returnSession['end_date'] = unix_time_millis(lolol.end_date)
        returnSession['course_id'] = lolol.course_id
        returnSession['sessionEff'] = lolol.sessionEff
        returnSession['sessionTemp'] = lolol.sessionTemp
        returnSession['sessionIll'] = lolol.sessionIll
        returnSession['sessionSound'] = lolol.sessionSound
        returnSession['sessionFocus'] = lolol.sessionFocus
        returnSession['sessionHum'] = lolol.sessionHum    
        
        returnList.append(returnSession)
    
    return json.dumps(returnList)
