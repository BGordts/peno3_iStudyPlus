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
from app.models.userStatitics import Userstatistic

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    feedback_score = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    pauzes = db.Column(db.String)
    puazed = db.Column(db.Boolean) #Is the running session pauzed?
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sessions', lazy='dynamic'))

    sessionEff = db.Column(db.Float)
    sessionTemp = db.Column(db.Float)
    sessionIll = db.Column(db.Float )
    sessionSound = db.Column(db.Float)
    sessionFocus = db.Column(db.Float)
    sessionHum = db.Column(db.Float)
    sessionIll = db.Column(db.Integer)
    sessionSound = db.Column(db.Integer)
    sessionFocus = db.Column(db.Integer)
    sessionHum = db.Column(db.Integer)
    
    def __init__(self, title, user, feedback_score = -1):
        self.title = title
        self.user = user
        self.pauzes = json.dumps([])
        self.pauzed = False
        self.start_date = None
        self.end_date = None
        self.feedback_score = feedback_score
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
    def startPauze(self):
        self.pauzed = True
        db.session.commit()
        
        session['isPauzed'] = time.time()
            
    '''
    End the timer of a puaze and store the puazeduration in the database
    '''
    def endPauze(self):
        self.pauzed = False
        
        pauze = json.loads(self.pauzes)
        pauze.append( (session['isPauzed'],time.time()) )
        self.pauzes = json.dumps(pauze)  
        
        db.session.commit()
        
        session['isPauzed'] = None
        
    def isPauzed(self):
        return self.pauzed
                 
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
        self.calcSessionTemp()
        self.calcSessionHum()
        self.calcSessionSound()
        self.calcSessionIll()
        self.calcSessionFocus()
        self.calcSessionEff()
        self.user.updateStatistics(self)
           
    def calcSessionEff(self):
        self.sessionEff = (self.sessionFocus + self.feedback_score)/2
        db.session.commit()
  
    def calcSessionHum(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="humidity").all()
        avHum = 0
        for hum in tempdata:
            avHum = avHum + hum.value
        self.sessionHum = avHum/(len(tempdata))
        db.session.commit()
        tempdata = SensorData.query.filter_by(session_id == self.id and sensor_type == temperature).all()
        
    def calcSessionTemp(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="temperature").all()
        avTemp = 0
        for temp in tempdata:
            avTemp = avTemp + temp.value
        self.sessionTemp = avTemp/(len(tempdata))
        db.session.commit()
        
    def calcSessionSound(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="sound").all()
        avSound = 0
        for sound in tempdata:
            avSound = avSound + sound.value
        self.sessionSound = avSound/(len(tempdata))
        db.session.commit()

    def calcSessionIll(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="illumination").all()
        avIll = 0
        for ill in tempdata:
            avIll = avIll + ill.value
        self.sessionIll = avIll/(len(tempdata))
        db.session.commit()
        
    def calcSessionFocus(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="focus").all()
        avFocus = 0
        for focus in tempdata:
            if(focus.value == 1):
                avFocus = avFocus + 1
        self.sessionFocus = avFocus/(len(tempdata))
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
        return '<Session %r>' % self.title