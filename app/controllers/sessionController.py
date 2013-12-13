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

from app.controllers.filters import login_required
from app.controllers.filters import logout_required
from app.controllers.filters import session_required
from app.controllers.filters import endSession_required

'''
Redirects to the sessions that's being tracked
'''
@app.route('/session/tracking')
@login_required
@session_required
def tracking():
    userSession = UserSession.query.get(session["sessionID"])
    
    state = "active"
    
    if userSession.end_date:
        state = "end"
    elif userSession.isPaused():
        state = "pause"
    #_log("info", "sessino: " + session['sessionID']);
    return render_template('pages/tracking_page.html', state = state)

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
    from datetime import datetime
    feedback_text = request.args["feedback"]
    start_date = datetime.fromtimestamp(float(request.args["start_time"])/1000)
    end_date = datetime.fromtimestamp(float(request.args["end_time"])/1000)
    user = User.getUserFromSession()
    usession = UserSession(user, course , description, feedback_text, start_date, end_date)
    db.session.add(usession)
    db.session.commit()
    return "ok"
    
@app.route('/session/modifyUSession' , methods = ['POST' , 'GET'])
@login_required
@endSession_required
def modifyUSession():
    uSession = UserSession.query.get(request.args['sessionID'])
    newDescription = uSession.description
    newFeedBack_score = uSession.feedback_score
    newStart_date = uSession.start_date
    newEnd_date = uSession.end_date
    newCourse = Course.query.get(request.args["courseID"])
    if not(newDescription == request.args['description']):
        newDescription = request.args['description']
    if not(newFeedBack_score == request.args['feedback']):
        newFeedBack_score = request.args['feedback']
    from datetime import datetime
    if not(newStart_date == datetime.fromtimestamp(float(request.args['startDate'])/1000)):
        newStart_date = datetime.fromtimestamp(float(request.args['startDate'])/1000)
    if not(newEnd_date == datetime.fromtimestamp(float(request.args['endDate'])/1000)):
        newEnd_date = datetime.fromtimestamp(float(request.args['endDate'])/1000)
    newSession = UserSession(uSession.user, newCourse, newDescription, newFeedBack_score, newStart_date, newEnd_date)
    oldId =uSession.id
    uSession.deleteUntrackedSession()
    db.session.delete(uSession)
    db.session.commit()
    newSession.id = oldId
    db.session.add(newSession)
    db.session.commit()
    
    return "done"
    
@app.route('/session/modifyTSession' , methods = ['POST' , 'GET'])
@login_required
def modifyTSession():
    sessionID = request.args["sessionID"]
    newDescription = request.args["description"]
    courseID = request.args["courseID"]
    
    userSession = UserSession.query.get(sessionID)
    userSession.description = newDescription
    userSession.course = Course.query.get(courseID)
    
    db.session.commit()
    
    return "done"

@app.route('/session/deleteUSession' , methods = ['POST' , 'GET'])
@login_required
@endSession_required
def deleteUSession():
    uSession = UserSession.query.get(request.args['sessionID'])
    uSession.deleteUntrackedSession()      
    
    return "deleted" 

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
    
    #sessionID = session.pop('sessionID',None)
    #session.pop('isPauzed',None)
    
    return json.dumps(sessionID)

@app.route('/session/postFeedback' , methods = ['GET'])
@login_required
def postFeedback():
    #_log("info", "input= " + request.args['sessionID'])
    #_log("info", "input= " + request.args['feedback'])
    #sessionID = request.args['sessionID']
    feedback = request.args['feedback']
    
    sessionID = session['sessionID']
    
    UserSession.query.get(sessionID).setFeedback(feedback)
    return "ok"

@app.route('/session/commit', methods = ['GET'])    
@login_required
def commitSession():
    sessionID = session['sessionID']
    userSession = UserSession.query.get(sessionID)
    _log("info", "mr usersessio: " + userSession.__str__())
    userSession.commitSession()
    
    sessionID = session.pop('sessionID',None)
    session.pop('isPauzed',None)
    
    #return redirect("app/" + session["userID"].__str__() + "/dashboard")
    return "Yolo"

'''
Returns all the sessions created by this user
'''
@app.route('/session/getAllSessions', methods = ['GET'])    
@login_required
def getAllSessions():
    userID = request.args["userID"]
    
    user = User.query.get(userID);
    
    _log("info", user.sessions.all().__str__())
    
    #Move to UserSesssion
    returnList = []
    for nextSession in user.sessions.all():        
        returnList.append({"sessionID":nextSession.id, "sessionData":nextSession.outputSession()})
    
    return json.dumps(returnList)
