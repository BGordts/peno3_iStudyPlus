from flask import *

from app import app
from app import db

import json

class Statistic(db.Model):
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
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sessionTemp
            i = i + 1
        return temp/(i-1)
    
    def getHigestTemp(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sessionTemp
            i = i + 1
        return temp/(i-1)
    
    def getLowestEff(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sessionEff
            i = i + 1
        return temp/(i-1)
    
    def getHigestEff(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sessionEff
            i = i + 1
        return temp/(i-1)
    
    def getLowestHum(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sessionHum
            i = i + 1
        return temp/(i-1)
    
    def getHigestHum(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sessionHum
            i = i + 1
        return temp/(i-1)
    
    def getLowestIll(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sessionIll
            i = i + 1
        return temp/(i-1)
    
    def getHigestIll(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sessionIll
            i = i + 1
        return temp/(i-1)
    
    def getLowestFocus(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sessionFocus
            i = i + 1
        return temp/(i-1)
    
    def getHigestFocus(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sessionFocus
            i = i + 1
        return temp/(i-1)
    
    def getLowestSound(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = UserSession.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sessionSound
            i = i + 1
        return temp/(i-1)
    
    def getHigestSound(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = UserSession.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sessionSound
            i = i + 1
        return temp/(i-1)
    
 
    