from flask import *

from app import app
from app import db

from app.models.session import Session
import json

class Userstatistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , unique =True)
    user = db.relationship('User', backref=db.backref('userStatistics', lazy='dynamic'))
    
    totalTime = db.Column(db.Float)
    
    totalEff = db.Column(db.Float)
    totalTempAv = db.Column(db.Float)
    totalIllum = db.Column(db.Float )
    totalSound = db.Column(db.Float)
    totalfocus = db.Column(db.Float)
    totalHumAv = db.Column(db.Float)
    
    lowestSessions = db.Column(db.String)
    highestSessions = db.Column(db.String)
    
    def __init__(self, user):
        self.user = user
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
        self.totalEff = dataWeight * self.totalEff + sessionWeight * userSession.getEff()
        self.totalfocus = dataWeight * self.totalfocus + sessionWeight * userSession.getFocus()
        self.totalHumAv = dataWeight * self.totalHumAv + sessionWeight * userSession.getHum()
        self.totalIllum = dataWeight * self.totalIllum + sessionWeight * userSession.getIll()
        self.totalSound = dataWeight * self.totalSound + sessionWeight * userSession.getSound()
        self.totalTempAv = dataWeight * self.totalTempAv + sessionWeight * userSession.getTemp()
        db.session.commit()
    
    def updateLowestSessions(self, userSession):
        lowestSessions = json.loads(self.lowestSessions)
        if(len(lowestSessions) < 5):
            lowestSessions.extends(userSession.id)
        else:
            highest = 0
            i = 1
            while i <= 5:
                hSession = Session.query.filter_by(id=lowestSessions[highest].id).first()
                iSession = Session.query.filter_by(id=lowestSessions[i].id).first()
                if(iSession.eff > hSession.eff ):
                    highest = i
                i = i + 1
            hSession = Session.query.filter_by(id=lowestSessions[highest].id).first()
            if(hSession.eff > userSession.eff):
                lowestSessions[highest] = userSession.id
        json.dumps(lowestSessions)
        db.session.commit()
                    
            
    def updateHighestSessions(self, userSession):
        highestSessions = json.loads(self.highestSessions)
        if(len(lowestSessions) < 5):
            lowestSessions.extends(userSession.id)
        else:
            lowest = 0
            i = 1
            while i <= 5:
                lSession = Session.query.filter_by(id=highestSessions[lowest].id).first()
                iSession = Session.query.filter_by(id=lowestSessions[i].id).first()
                if(iSession.eff < lSession.eff ):
                    lowest = i
                i = i + 1
            lSession = Session.query.filter_by(id=highestSessions[lowest].id).first()
            if(lSession.eff < userSession.eff):
                highestSessions[lowest] = userSession.id
        json.dumps(highestSessions)
        db.session.commit()
      
  
    def getLowestTemp(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = Session.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.temp
            i = i + 1
        return temp/(i-1)
    
    def getHigestTemp(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = Session.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.temp
            i = i + 1
        return temp/(i-1)
    
    def getLowestEff(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = Session.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.eff
            i = i + 1
        return temp/(i-1)
    
    def getHigestEff(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = Session.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.eff
            i = i + 1
        return temp/(i-1)
    
    def getLowestHum(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = Session.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.hum
            i = i + 1
        return temp/(i-1)
    
    def getHigestHum(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = Session.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.hum
            i = i + 1
        return temp/(i-1)
    
    def getLowestIll(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = Session.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.ill
            i = i + 1
        return temp/(i-1)
    
    def getHigestIll(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = Session.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.ill
            i = i + 1
        return temp/(i-1)
    
    def getLowestFocus(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = Session.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.focus
            i = i + 1
        return temp/(i-1)
    
    def getHigestFocus(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = Session.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.focus
            i = i + 1
        return temp/(i-1)
    
    def getLowestSound(self):
        lowestSessions = json.loads(self.lowestSessions)
        i = 0
        temp = 0
        while(i < len(lowestSessions)):
            lSession = Session.query.filter_by(id=lowestSessions[i].id).first()
            temp = temp + lSession.sound
            i = i + 1
        return temp/(i-1)
    
    def getHigestSound(self):
        highestSessions = json.loads(self.highestSessions)
        i = 0
        temp = 0
        while(i < len(highestSessions)):
            lSession = Session.query.filter_by(id=highestSessions[i].id).first()
            temp = temp + lSession.sound
            i = i + 1
        return temp/(i-1)
    
    