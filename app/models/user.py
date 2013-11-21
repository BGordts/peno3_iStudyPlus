from flask import *

from app import app
from app import db

from app.models.session import Session

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80), unique=False)
    surname = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(30), unique=False)

    def __init__(self, email, name, surname, password):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password    
    
    @staticmethod
    def getAdminUser():
        return User.query.filter_by(id = 1).first()   
    
    @staticmethod
    def getUserFromSession():
        return User.getUserByID(session['userID'])
    
    def getProfilePic(self):
        pass
    
    def setProfilePic(self):
        pass
    
    @staticmethod
    def getUserByID(ID):
        return User.query.filter_by(id = ID).first()
    
    def getRunningSession(self):
        if session['sessionID']:
            if session['isPauzed']:
                return Session.getSessionByID(session['sessionID'])
        return None
    
    def changeSetting(self):
        pass
       
    def getUsers(self):
        pass
    
    def __repr__(self):
        return '<User %r>' % self.email