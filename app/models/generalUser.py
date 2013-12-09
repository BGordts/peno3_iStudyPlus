from flask import *

from app import app
from app import db

from werkzeug._internal import _log
from app.models.statistics import Statistics
from app.models.userSession import UserSession

class GeneralUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    userStastics_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    statistics = db.relationship('Statistics', backref=db.backref('generalUser', lazy='dynamic'))
    
    nbSessions = db.Column(db.Integer)
    
    def __init__(self):
        newUS = Statistics()
        db.session.add(newUS)
        self.statistics = newUS
        db.session.commit()
        self.nbSessions = 0
    
    @staticmethod
    def updateGeneralCase(userSession):
        if(GeneralUser.query.first() == None):
            db.session.add(GeneralUser())
        GeneralUser.query.first().updateStatistics(userSession)
    
    def updateStatistics(self,userSession):
        n = self.nbSessions
        self.statistics.updateGeneralStatistic(n ,userSession)
        userSession.course.updateStatistic(userSession)
        self.nbSessions = n + 1
    
from app.models.course import Course