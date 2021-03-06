from flask import *

from app import app
from app import db

from werkzeug._internal import _log
from app.models.statistics import Statistics
from app.models.userSession import UserSession
from app.models.device import Device
from app.models.generalUser import GeneralUser

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80), unique=False)
    surname = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(30), unique=False)
    study = db.Column(db.String(30))
    
    picBig = db.Column(db.String(150000))
    picSmall = db.Column(db.String(5000))
    
    userStastics_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    statistics = db.relationship('Statistics', backref=db.backref('users', lazy='dynamic'))
    
    def __init__(self, email, name, surname, password, study, deviceID=None, profilePic_small = None , profilePic_big = None ):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password
        self.study = study
        Course.addUserCoursesStudy(self, study)
        Device.registerDevice(deviceID, self)
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
        self.statistics.updateStatistics(userSession)
        GeneralUser.updateGeneralCase(userSession)   
    
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
        userSession = UserSession.query.filter_by(user=self).filter_by(end_date=None).order_by(UserSession.start_date.desc()).first()
        
        # See if there is a session and the session is already started
        if userSession and userSession.start_date:
            # If the end_date is set, the session is ended and there is no currently running session
            if(userSession.end_date):
                return None
            else:
                return userSession
        else:
            return None

    def getDevice(self):
        return self.device.first()
    
    def changeSetting(self , email , name , surname , password,study,deviceID,pic_small,pic_big):
        if not (email == self.email):
            self.email = email
        if not (name == self.name):
            self.name = name    
        if not (surname == self.surname):
            self.surname = surname
        if not (password == self.password):
            self.password = password
        if not (pic_small == self.picSmall):
            self.picSmall = pic_small
        if not (pic_big == self.picBig):
            self.picBig = pic_big
        db.session.commit()       
        Device.query.filter_by(user=self).first().key = deviceID
        db.session.commit()
    
    def outputLarge(self):
        returndict = {}
        
        returndict["userID"] = self.id
        returndict["name"] = self.name
        returndict["surname"] = self.surname
        returndict["pic_big"] = self.picBig
        returndict["pic_small"] = self.picSmall
        returndict["study"] = self.study
        
        return returndict
    
    def outputSmall(self):
        returndict = {}
        
        returndict["userID"] = self.id
        returndict["name"] = self.name
        returndict["surname"] = self.surname
        returndict["pic_small"] = self.picSmall
        
        return returndict
    
from app.models.course import Course