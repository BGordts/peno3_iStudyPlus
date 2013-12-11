from __future__ import division
from flask import *
from flask.ext.sqlalchemy import SQLAlchemy 
from werkzeug._internal import _log

import time
import datetime
import json

from app import app
from app import db
from sqlalchemy.dialects.sqlite.base import DATE
from app.models.sensordata import Sensordata

from app.utils.utils import *
from app.models.courseUsers import Courses_Users

class UserSession(db.Model):
    __tablename__ = 'usersessions'
    id = db.Column(db.Integer, primary_key=True)
    
    description = db.Column(db.String(250))
    feedback_text = db.Column(db.String(160))
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
    
    def __init__(self, user, course , description , feedback_score = None, start_date =None, end_date=None):
        self.description = description
        self.feedback_text = None
        self.user = user
        self.course = course
        self.pauses = json.dumps([])
        #self.paused = False
        self.start_date = start_date
        self.end_date = end_date
        self.feedback_score = feedback_score
        self.sessionEff = 0
        self.sessionTemp = 0
        self.sessionIll = 0
        self.sessionSound = 0
        self.sessionFocus = 0
        self.sessionHum = 0
        if not (end_date== None):
            user.statistics.addUntrackedSession(self)
            CUStatistic = Courses_Users.query.filter_by(course=self.course,user=self.user).first().courseStatistics
            CUStatistic.addUntrackedSession(self)

    def deleteUntrackedSession(self):
        self.user.statistics.deleteUntrackedSession(self)
        CUStatistic = Courses_Users.query.filter_by(course=self.course).first().courseStatistics
        CUStatistic.deleteUntrackedSession(self)
        db.session.delete(self)
        db.session.commit()
        
    '''
    Start the timer of the session
    '''
    def start(self):
        self.start_date = datetime.now()
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
        if(self.isPaused()):
            self.endPause()
        if not self.start_date == None:
            self.end_date = datetime.now()
        else:
            db.session.delete(self)
        db.session.commit()

    def commitSession(self):
        self.calcSessionTemp()
        self.calcSessionHum()
        self.calcSessionSound()
        self.calcSessionIll()
        self.calcSessionFocus()
        self.calcSessionEff()
        self.user.updateStatistics(self)
        CUStatistic = Courses_Users.query.filter_by(course=self.course,user=self.user).first().courseStatistics
        CUStatistic.updateStatistics(self)
        db.session.commit()
        
    def outputSensorData(self, sensor):
        loadedPauses = json.loads(self.pauses)
        
        nextPause = None
        nextPauseIndex = 0
        
        if len(loadedPauses) > 0:
            nextPause = float(loadedPauses[0][0])
        sensorData = Sensordata.query.filter_by(userSession=self).filter_by(sensor_type=sensor).all()
        returnList = []
        
        for i in range(0,len(sensorData)):                 
            if nextPause and nextPause < unix_time_millis(sensorData[i].date):
                returnList.append({"sensor_type": sensor, "value": None, "date": nextPause, "session_id": self.id})
                nextPauseIndex += 1
                
                if nextPauseIndex < len(loadedPauses):
                    nextPause = float(loadedPauses[nextPauseIndex][0])
                else:
                    nextPause = None
                    
            returnList.append(sensorData[i].output())
            
        return returnList
    
    def outputSensorDataXY(self, sensor):
        loadedPauses = json.loads(self.pauses)
        
        nextPause = None
        nextPauseIndex = 0
        
        if len(loadedPauses) > 0:
            nextPause = float(loadedPauses[0][0])        
        sensorData = Sensordata.query.filter_by(userSession=self).filter_by(sensor_type=sensor).all()
        returnList = []
        
        for i in range(0,len(sensorData)):   
            if nextPause and nextPause < unix_time_millis(sensorData[i].date):
                returnList.append({"x": nextPause, "y":None})
                nextPauseIndex += 1
                
                if nextPauseIndex < len(loadedPauses):
                    nextPause = float(loadedPauses[nextPauseIndex][0])
                else:
                    nextPause = None
                    
            returnList.append(sensorData[i].outputXY())
            
        return returnList
    
    def outputSession(self):
        returnSession = {}
        returnSession['description'] = self.description
        returnSession['feedback_text'] = self.feedback_text
        returnSession['feedback_score'] = self.feedback_score
        returnSession['start_date'] = unix_time_millis(self.start_date)
        returnSession['end_date'] = unix_time_millis(self.end_date)
        returnSession['course_id'] = self.course_id
        returnSession['sessionEff'] = self.sessionEff
        returnSession['sessionTemp'] = self.sessionTemp
        returnSession['sessionIll'] = self.sessionIll
        returnSession['sessionSound'] = self.sessionSound
        returnSession['sessionFocus'] = self.sessionFocus
        returnSession['sessionHum'] = self.sessionHum
        
        return returnSession
           
    def calcSessionEff(self):
        self.sessionEff = (self.sessionFocus + self.feedback_score)/2
    def calcSessionHum(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="humidity").all()
        self.sessionHum = calculate_average([x.value for x in tempdata])
    def calcSessionTemp(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="temperature").all()
        self.sessionTemp = calculate_average([x.value for x in tempdata])    
    def calcSessionSound(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="sound").all()
        self.sessionSound = calculate_average([x.value for x in tempdata])
    def calcSessionIll(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="illumination").all()
        self.sessionIll = calculate_average([x.value for x in tempdata])      
    def calcSessionFocus(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="focus").all()
        self.sessionFocus = calculate_average([x.value for x in tempdata])
    
    '''
    geeft de totale duur van de sessie in seconden
    '''
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
