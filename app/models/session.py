from flask import *
from flask.ext.sqlalchemy import SQLAlchemy 
from werkzeug._internal import _log
from datetime import datetime

from app import app
from app import db

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    feedback_score = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sessions', lazy='dynamic'))

    def __init__(self, title, user, feedback_score = -1):
        self.title = title
        self.user = user
        self.start_date = None
        self.end_date = None
        self.feedback_score = feedback_score
        
    
    def start(self):
        self.start_date = datetime.utcnow()
        db.session.commit()
    
    def end(self):
        self.end_date = datetime.utcnow()  
        db.session.commit()
        
    @classmethod
    def getSessionByID(sessionID):
        return Session.query.filter_by(id = sessionID).first()
        
    def __repr__(self):
        return '<Session %r>' % self.title