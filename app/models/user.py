from flask import *

from app import app
from app import db

from app.models.session import Session
from werkzeug._internal import _log
from app.models.statistics import Statistic
from app.models.Association import Courses_Users


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80), unique=False)
    surname = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(30), unique=False)
    profilePic = db.Column(db.String(300), unique = True)
    
    userStastic_id = db.Column(db.Integer, db.ForeignKey('statistic.id'))
    statistic = db.relationship('Statistic', backref=db.backref('users', lazy='dynamic'))
    
    
    def __init__(self, email, name, surname, password, profilePic = None):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password
        self.profilePic = profilePic
        newUS = Statistic()
        db.session.add(newUS)
        self.statistic = newUS
    
    def getUserCourses(self):
        userCourses = []
        for course in Course.query.all():
            if course.hasAsUser(self):
                userCourses.append(course)
        return userCourses
    
    def updateStatistics(self,userSession):
        self.statistic.updateUserStatistics(userSession)   
    
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
    
    def getRunningSession(self):
        if session['sessionID']:
            if session['isPauzed']:
                return Session.getSessionByID(session['sessionID'])
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
    
    def getUsers(self):
        "enkel users met dezelfde vakken als de huidige gebruiker."
        pass
    
    def __repr__(self):
        return '<User %r>' % self.email
    
from app.models.course import Course