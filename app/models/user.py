from flask import *

from app import app
from app import db

from app.models.session import Session
from app.models.course import Course
from werkzeug._internal import _log

users_courses = db.Table('users_courses',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80), unique=False)
    surname = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(30), unique=False)
    profilePic = db.Column(db.String(300), unique = True)
    courses = db.relationship('Course', secondary=users_courses,backref=db.backref('courses', lazy='dynamic'))
    
    def __init__(self, email, name, surname, password, profilePic = None):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password
        self.profilePic = profilePic
        self.courses = []
          
    def addCourse(self , course):
        self.courses.append(Course(course))
        
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
    
    def getRunningsession2(self):
        session = Session.query.filter_by(user=self).order_by(Session.start_date.desc()).first()
        
        if(session.end_date):
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
    
    def getUsers(self):
        "enkel users met dezelfde vakken als de huidige gebruiker."
        pass
    
    def __repr__(self):
        return '<User %r>' % self.email