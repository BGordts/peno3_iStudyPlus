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

'''
een userSession is een klasse met id, beschrijving, feedback text, feedback score,
start date, eind datum,pauzes, gepauzeerd,cursus, gebruiker, sessie efficientie,
sessie temperatuur, sessie belichting,sessie geluid, sessie focus en
sessie vochtigheid. 
'''
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
    
    '''
    initialiseert een user session object.
    
    @param User user: de user voor deze UserSession.
    @param Course course: de cursus voor deze UserSession.
    @param String description: de beschrijving voor deze UserSession.
    @param Integer feedback_score: de feedback score voor deze userSession,
           deze is standaard None.
    @param Datetime start_date: de start datum voor deze UserSession, deze is standaard None.
    @param Datetime end_date: de eind datum voor deze UserSession, deze is standaard None.
    
    @postcondition: de user van deze userSession is gelijk aan user.
    @postcondition: de course van deze userSession is gelijk aan course.
    @postcondition: de beschrijving van deze userSession is gelijk aan description.
    @postcondition: de feedback score van deze userSession is gelijk aan feedback_score
                    of None.
    @postcondition: de start datum score van deze userSession is gelijk aan start_datum
                    of None.
    @postcondition: de eind datum van deze userSession is gelijk aan end_date of None.
    
    @postcondition: Als end_datum niet gelijk is aan None, dan wordt de userSession
                    toegevoegd de course statistics en userStatistics.
    @postcondition: Dit userSession object wordt toegevoegd aan de database.
    '''
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
    '''
    verwijdert een niet getrackte sessie uit de database.
    
    @postcondition: de gegevens worden uit de userStatistics gehaald.
    @postcondition: de gegevens worden uit de user_cours statistics gehaald.
    @postcondition: het userSession object wordt uit de database verwijdert.
    '''
    def deleteUntrackedSession(self):
        self.user.statistics.deleteUntrackedSession(self)
        CUStatistic = Courses_Users.query.filter_by(course=self.course).first().courseStatistics
        CUStatistic.deleteUntrackedSession(self)
        db.session.delete(self)
        db.session.commit()
        
    '''
    start de timer van deze sessie.
    
    @postcondition:de starttijd van deze sessie is gelijk aan de huidige tijd.
    '''
    def start(self):
        self.start_date = datetime.now()
        db.session.commit()
        
    '''
    start de pauze van deze sessie.
    
    @postcondition: de sessie is gepauzeerd.
    '''
    def startPause(self):
        self.paused = True
        db.session.commit()
        
        session['isPauzed'] = time.time()
            
    '''
    beëindigd de pauze.
    
    @postcondition: de sessie is terug hervat.
    @postcondition: de volledige pauze is toegevoegd aan de userSession.
    '''
    def endPause(self):
        self.paused = False
        
        pauze = json.loads(self.pauses)
        pauze.append( (session['isPauzed'],time.time()) )
        self.pauses = json.dumps(pauze)  
        
        db.session.commit()
        
        session['isPauzed'] = None

    '''
    controleerd of deze userSession gepauzeerd is.
    
    @return: True als de sessie gepauzeerd is en False als de sessie aan het draaien is.
    '''    
    def isPaused(self):        
        return self.paused
                 
    '''
    beëindigd de timer van de sessie.
    
    @postcondition: als de start tijd niet None is, is de eind tijd van de
                    sessie is gelijk aan de huidige tijd.
    @postcondition: als de pauze nog gepauzeerd was, is de pauze ook beëindigd.
    @postcondition: als de start tijd van deze sessie None is, wordt de sessie
                    verwijdert uit de database.
    '''
    def end(self):
        if(self.isPaused()):
            self.endPause()
        if not self.start_date == None:
            self.end_date = datetime.now()
        else:
            db.session.delete(self)
        db.session.commit()

    '''
    berekent de gemiddelde waarden van de temperatuur, vochtigheid, geluid,
    lichtsterkte,focus en efficientie. Ook de userStatistieken en de course
    user statistieken worden geupdate.
    
    @postcondition: het gemiddelde van de temperatuur data van deze sessie is berekent.
    @postcondition: het gemiddelde van de vochtigheid data van deze sessie is berekent.
    @postcondition: het gemiddelde van het geluid data van deze sessie is berekent.
    @postcondition: het gemiddelde van de belichting data van deze sessie is berekent.
    @postcondition: het gemiddelde van de focus data van deze sessie is berekent.
    @postcondition: de efficientie van deze sessie is berekent.
    
    @postcondition: de course user statistic is geupdate
    @postcondition: de user statistic is geupdate
    '''
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
    
    '''
    geeft een lijst terug waarin dictionaries staan van de te plotten data,
    met x-key: de tijd en y-key:de sensorwaarde.
    
    @param String sensor: het type sensor waarvoor de waarden moeten worden teruggeven.
    @return: een lijst met dictionaries waarin het tijdsstip en de sensorwaarde staat.
    '''
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
    
    '''
    geeft een dictionary met al de data van deze sessie terug.
    
    @return: een dictionary terug met de beschrijving, feedback text, feedback score,
             start datum, eind datum, course id, efficientie, gemiddelde temperatuur,
             gemiddelde belichting, gemiddelde geluid, gemiddelde focus en gemiddelde
             vochtigheid van deze sessie. 
    '''
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
    
    '''
    berekent de gemiddelde efficientie van deze sessie.
    
    @precondition: de session focus en de session feedback is niet 0.
    @postcondition: de nieuwe efficientie is gelijk aan de (sessionFocus+feedback_score)/2.
    '''      
    def calcSessionEff(self):
        self.sessionEff = (self.sessionFocus + self.feedback_score)/2
        
    '''
    berekent de gemiddelde vochtigheid van deze sessie.
    
    @postcondition: de session vochtigheid van deze sessie is het gemiddelde
                    van al de vochtigheid data.
    '''
    def calcSessionHum(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="humidity").all()
        self.sessionHum = calculate_average([x.value for x in tempdata])
        
    '''
    berekent de gemiddelde temperatuur van deze sessie.
    
    @postcondition: de session temperatuur van deze sessie is het gemiddelde
                    van al de temperatuur data.
    '''
    def calcSessionTemp(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="temperature").all()
        self.sessionTemp = calculate_average([x.value for x in tempdata])    
    
    '''
    berekent het gemiddelde geluid van deze sessie.
    
    @postcondition: het session geluid van deze sessie is het gemiddelde van al
                    de geluids data.
    '''
    def calcSessionSound(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="sound").all()
        self.sessionSound = calculate_average([x.value for x in tempdata])
    
    '''
    berekent de gemiddelde belichting van deze sessie.
    
    @postcondition: de session illumination van deze sessie is het gemiddelde
                    van al de belichting data.
    '''
    def calcSessionIll(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="illumination").all()
        self.sessionIll = calculate_average([x.value for x in tempdata])      
    
    '''
    berekent de gemiddelde focus van deze sessie.
    
    @postcondition: de session focus van deze sessie is het gemiddelde van al de focus data.
    '''
    def calcSessionFocus(self):
        tempdata = Sensordata.query.filter_by(session_id=self.id, sensor_type="focus").all()
        self.sessionFocus = calculate_average([x.value for x in tempdata])
    
    '''
    geeft de totale duur van de sessie in seconden.
    
    @return: de tijdsduur van deze sessie.
    '''
    def getSessionDuration(self):
        deltaTime = self.end_date - self.start_date
        duration = deltaTime.total_seconds()
        return duration
    
    '''
    de feedback score van deze sessie is gelijk aan score.
    
    @param Integer score: de feedback score van deze sessie.
    @postcondition: de feedback_score van deze sessie is gelijk aan score.
    '''
    def setFeedback(self, score):
        self.feedback_score = score
        db.session.commit()
    
    '''
    geeft het userSession object terug gelinkt aan het gegeven sessionID.
    
    @return: de userSession met gegeven sessionID.
    '''    
    @classmethod
    def getSessionByID(sessionID):
        return Session.query.filter_by(id = sessionID).first()
