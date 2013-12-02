from __future__ import division
from flask import *
from flask.ext.sqlalchemy import SQLAlchemy 
from werkzeug._internal import _log

import time
from datetime import datetime
import json

from app import app
from app import db
from sqlalchemy.dialects.sqlite.base import DATE
from app.models.sensordata import Sensordata

from app.utils.utils import *

class UserSession(db.Model):
    __tablename__ = 'usersessions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    feedback_score = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    pauses = db.Column(db.String)
    paused = db.Column(db.Boolean, default=False) #Is the running session paused?
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref=db.backref('sessions', lazy='dynamic'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sessions', lazy='dynamic'))

    sessionEff = db.Column(db.Float)
    sessionTemp = db.Column(db.Float)
    sessionIll = db.Column(db.Float )
    sessionSound = db.Column(db.Float)
    sessionFocus = db.Column(db.Float)
    sessionHum = db.Column(db.Float)
    
    def __init__(self, user, course , title):
        self.title = title
        self.user = user
        self.course = course
        self.pauses = json.dumps([])
        #self.paused = False
        self.start_date = None
        self.end_date = None
        self.feedback_score = -1
        self.sessionEff = 0
        self.sessionTemp = 0
        self.sessionIll = 0
        self.sessionSound = 0
        self.sessionFocus = 0
        self.sessionHum = 0
        
    '''
    Start the timer of the session
    '''
    def start(self):
        self.start_date = datetime.utcnow()

        db.session.commit()
        
    '''
    Start the timer of a pauze
    '''
    def startPause(self):
        self.paused = True
        db.session.commit()
        
        session['isPauzed'] = time.time()
            
    '''
    End the timer of a puaze and store the puazeduration in the database
    '''
    def endPause(self):
        self.paused = False
        
        pauze = json.loads(self.pauses)
        pauze.append( (session['isPauzed'],time.time()) )
        self.pauses = json.dumps(pauze)  
        
        db.session.commit()
        
        session['isPauzed'] = None
        
    def isPaused(self):        
        return self.paused
                 
    '''
    End the timer of the session
    '''
    def end(self):
        if(not session['isPauzed'] == None):
            self.endPauze()
        if not self.start_date == None:
            self.end_date = datetime.utcnow()
        else:
            db.session.delete(self)
        db.session.commit()
    
    def commitSession(self):
        _log("info", "commiting")
        self.calcSessionTemp()
        self.calcSessionHum()
        self.calcSessionSound()
        self.calcSessionIll()
        self.calcSessionFocus()
        self.calcSessionEff()
        self.user.updateStatistics(self)
        
    def outputSensorData(self, sensor):
        sensorData = Sensordata.query.filter_by(session=self).filter_by(sensor_type=sensor).all()
        
        _log("info", "sensordata: " + sensorData[0].__str__())
        returnList = []
        
        for i in range(0,len(sensorData)):
            returnList.append(sensorData[i].output())       
        
        _log("info", "sensordata: " + returnList.__repr__())
        
        return returnList
           
    def calcSessionEff(self):
        self.sessionEff = (self.sessionFocus + self.feedback_score)/2
        db.session.commit()
  
    def calcSessionHum(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="humidity").all()
        _log("info", "tempdata: " + tempdata.__str__())
        self.sessionHum = calculate_average([x.value for x in tempdata])
        _log("info", "sessionHUM: " + self.sessionHum.__str__())
        db.session.commit()
        
    def calcSessionTemp(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="temperature").all()
        _log("info", "tempdata: " + tempdata.__str__())
        self.sessionTemp = calculate_average([x.value for x in tempdata])
        _log("info", "sessionTEMP: " + self.sessionTemp.__str__())
        db.session.commit()
        
    def calcSessionSound(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="sound").all()
        self.sessionSound = calculate_average([x.value for x in tempdata])
        db.session.commit()

    def calcSessionIll(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="illumination").all()
        self.sessionIll = calculate_average([x.value for x in tempdata])
        db.session.commit()
        
    def calcSessionFocus(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="focus").all()
        self.sessionFocus = calculate_average([x.value for x in tempdata])
        db.session.commit()
    
    def getSessionDuration(self):
        deltaTime = self.end_date - self.start_date
        duration = deltaTime.total_seconds()
        return duration
    
    def setFeedback(self, score):
        self.feedback_score = score
        db.session.commit()
        
    @classmethod
    def getSessionByID(sessionID):
        return Session.query.filter_by(id = sessionID).first()
        
    def __repr__(self):
        return '<UserSession %r>' % self.title