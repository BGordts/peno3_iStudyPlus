from flask import *
from flask.ext.sqlalchemy import SQLAlchemy 
from werkzeug._internal import _log
from datetime import datetime

import json

from app import app
from app import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('device', lazy='dynamic'))

    def __init__(self, key, user):
        self.key = key
        self.user = user
        
    def getUser(self):
        return self.user
    
    @staticmethod
    def registerDevice(device_key, user):
        device = user.getDevice()
        if(device):
            device.key = device_key
        else:
            device = Device(device_key, user)
            db.session.add(device)
            db.session.commit()    
   
    @staticmethod
    def getDeviceByKey(key):
        return Device.query.filter_by(key = key).first()
    
    def __repr__(self):
        return '<Device %r>' % self.key