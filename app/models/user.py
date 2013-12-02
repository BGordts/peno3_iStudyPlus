from flask import *

from app import app
from app import db

from werkzeug._internal import _log
from app.models.statistics import Statistics

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80), unique=False)
    surname = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(30), unique=False)
    
    picBig = db.Column(db.String(5000))
    picSmall = db.Column(db.String(1000))
    
    userStastics_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    statistics = db.relationship('Statistics', backref=db.backref('users', lazy='dynamic'))
    
    def __init__(self, email, name, surname, password, profilePic_small = None , profilePic_big = None):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password
        newUS = Statistics()
        db.session.add(newUS)
        self.statistics = newUS
        self.picBig = profilePic_big
        self.picSmall = profilePic_small     
        db.session.commit()
    
    def getUserCourses(self):
        userCourses = []
        for course in Course.query.all():
            if course.hasAsUser(self):
                userCourses.append(course)
        return userCourses
    
    def updateStatistics(self,userSession):
        self.statistics.updateUserStatistics(userSession)   
    
    @staticmethod
    def getAdminUser():
        return User.query.filter_by(id = 1).first()   
    
    @staticmethod
    def getUserFromSession():
        return User.getUserByID(session['userID'])
    
    def setProfilePic(self, path):
        self.profilePic = path
        db.session.commit()
    
    def getProfilePic(self):
        return self.profilePic
    
    @staticmethod
    def getUserByID(ID):
        return User.query.filter_by(id = ID).first()
    
    '''
    def getRunningSessionOld(self):
        if session['sessionID']:
            if session['isPauzed']:
                return UserSession.getSessionByID(session['sessionID'])
        return None
    '''
    
    def getRunningSession(self):
        session = UserSession.query.filter_by(user=self).order_by(UserSession.start_date.desc()).first()
        
        # See if there is a session and the session is already started
        if session and session.start_date:
            # If the end_date is set, the session is ended and there is no currently running session
            if(session.end_date):
                return None
            else:
                return session
        else:
            return None

    def getDevice(self):
        return self.device.first()
    
    def changeSetting(self , email , name , surname , password):
        if not (email == self.email):
            self.email = email
        if not (name == self.name):
            self.name = name    
        if not (surname == self.surname):
            self.surname = surname
        if not (password == self.password):
            self.password = password
        db.session.commit()
    
    def __repr__(self):
        return '<User %r>' % self.email
    
from app.models.course import Course