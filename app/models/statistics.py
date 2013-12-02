from flask import *
from werkzeug._internal import _log

from app import app
from app import db

#from session import UserSession

import json
from app.models.userSession import UserSession
from app.utils.utils import *

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    totalTime = db.Column(db.Float)
    
    totalEff = db.Column(db.Float)
    totalTempAv = db.Column(db.Float)
    totalIllum = db.Column(db.Float )
    totalSound = db.Column(db.Float)
    totalfocus = db.Column(db.Float)
    totalHumAv = db.Column(db.Float)
    
    lowestSessions = db.Column(db.String)
    highestSessions = db.Column(db.String)
    
    def __init__(self):
        self.totalTime = 0
        self.totalEff = -1
        self.totalTempAv = -1
        self.totalIllum = -1
        self.totalSound= -1
        self.totalfocus= -1
        self.totalHumAv = -1
        self.lowestSessions = json.dumps([])
        self.highestSessions = json.dumps([])        
    
    def updateUserStatistics(self,userSession):
        self.updateTotals(userSession)
        self.updateHighestSessions(userSession)
        self.updateLowestSessions(userSession)
    
        
    def updateTotals(self, userSession):
        oldTotalTime = self.totalTime
        self.totalTime = oldTotalTime + userSession.getSessionDuration()
        sessionWeight = userSession.getSessionDuration()/self.totalTime
        dataWeight = oldTotalTime/self.totalTime
        self.totalEff = dataWeight * self.totalEff + sessionWeight * userSession.sessionEff
        self.totalfocus = dataWeight * self.totalfocus + sessionWeight * userSession.sessionFocus
        self.totalHumAv = dataWeight * self.totalHumAv + sessionWeight * userSession.sessionHum
        self.totalIllum = dataWeight * self.totalIllum + sessionWeight * userSession.sessionIll
        self.totalSound = dataWeight * self.totalSound + sessionWeight * userSession.sessionSound
        self.totalTempAv = dataWeight * self.totalTempAv + sessionWeight * userSession.sessionTemp
        db.session.commit()
    
    def updateLowestSessions(self, userSession):
        lowestSessions = json.loads(self.lowestSessions)
        if(len(lowestSessions) < 5):
            lowestSessions.append(userSession.id)
        else:
            highest = 0
            i = 1
            while i <= 5:
                hSession = UserSession.query.filter_by(id=lowestSessions[highest].id).first()
                iSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
                if(iSession.sessionEff > hSession.sessionEff ):
                    highest = i
                i = i + 1
            hSession = UserSession.query.filter_by(id=lowestSessions[highest].id).first()
            if(hSession.sessionEff > userSession.sessionEff):
                lowestSessions[highest] = userSession.id
        self.lowestSessions = json.dumps(lowestSessions)
        db.session.commit()
                    
            
    def updateHighestSessions(self, userSession):
        highestSessions = json.loads(self.highestSessions)
        if(len(highestSessions) < 5):
            highestSessions.append(userSession.id)
        else:
            lowest = 0
            i = 1
            while i <= 5:
                lSession = UserSession.query.filter_by(id=highestSessions[lowest].id).first()
                iSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
                if(iSession.sessionEff < lSession.sessionEff ):
                    lowest = i
                i = i + 1
            lSession = UserSession.query.filter_by(id=highestSessions[lowest].id).first()
            if(lSession.sessionEff < userSession.sessionEff):
                highestSessions[lowest] = userSession.id
        self.highestSessions = json.dumps(highestSessions)
        db.session.commit()
        
        
    '''
    Makes a map with all the interesting data in this object. Used to render the json in the controllers.
    '''
    def outputData(self):
        returnData = {}
        
        returnData['total_time'] = self.totalTime
        returnData['total_efficiency'] = self.totalEff
        returnData['total_focus'] = self.totalfocus
        returnData['total_illumination_average'] = self.totalIllum
        returnData['total_temperature_average'] = self.totalTempAv
        returnData['total_sound_average'] = self.totalSound
        returnData['total_humidity_average'] = self.totalHumAv
        
        returnData['highest_illumination'] = self.getHigestIll()
        returnData['highest_temperature'] = self.getHigestTemp()
        returnData['highest_sound'] = self.getHigestSound()
        returnData['highest_humidity'] = self.getHigestHum()
        
        returnData['lowest_illumination'] = self.getLowestIll()
        returnData['lowest_temperature'] = self.getLowestTemp()
        returnData['lowest_sound'] = self.getLowestSound()
        returnData['lowest_humidity'] = self.getLowestHum()
        
        return returnData              
    
    def getLowestTemp(self):
        return calculate_average([UserSession.query.get(x).sessionTemp for x in json.loads(self.lowestSessions)])
    
    def getHigestTemp(self):
        return calculate_average([UserSession.query.get(x).sessionTemp for x in json.loads(self.highestSessions)])
    
    def getLowestEff(self):
        return calculate_average([UserSession.query.get(x).sessionEff for x in json.loads(self.lowestSessions)])
    
    def getHigestEff(self):
        return calculate_average([UserSession.query.get(x).sessionEff for x in json.loads(self.highestSessions)])
    
    def getLowestHum(self):
        return calculate_average([UserSession.query.get(x).sessionHum for x in json.loads(self.lowestSessions)])
    
    def getHigestHum(self):
        return calculate_average([UserSession.query.get(x).sessionHum for x in json.loads(self.highestSessions)])
    
    def getLowestIll(self):
        return calculate_average([UserSession.query.get(x).sessionIll for x in json.loads(self.lowestSessions)])
    
    def getHigestIll(self):
        return calculate_average([UserSession.query.get(x).sessionIll for x in json.loads(self.highestSessions)])
    
    def getLowestFocus(self):
        return calculate_average([UserSession.query.get(x).sessionFocus for x in json.loads(self.lowestSessions)])
    
    def getHigestFocus(self):
        return calculate_average([UserSession.query.get(x).sessionFocus for x in json.loads(self.highestSessions)])
    
    def getLowestSound(self):
        return calculate_average([UserSession.query.get(x).sessionSound for x in json.loads(self.lowestSessions)])
    
    def getHigestSound(self):
        return calculate_average([UserSession.query.get(x).sessionSound for x in json.loads(self.highestSessions)])
    
 
    