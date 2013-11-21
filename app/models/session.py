from flask import *
from flask.ext.sqlalchemy import SQLAlchemy 
from werkzeug._internal import _log
import time
from datetime import datetime
import json

from app import app
from app import db
from sqlalchemy.dialects.sqlite.base import DATE

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    feedback_score = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    pauzes = db.Column(db.String(500))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sessions', lazy='dynamic'))

    def __init__(self, title, user, feedback_score = -1):
        self.title = title
        self.user = user
        self.pauzes = json.dumps([])
        self.start_date = None
        self.end_date = None
        self.feedback_score = feedback_score
        
    def start(self):
        if(self.start_date == None):
            self.start_date = datetime.utcnow()
        else:
            self.endPauze()
        db.session.commit()
            
    def endPauze(self):
        pauze = json.loads(self.pauzes)
        pauze.append( (session['isPauzed'],time.time()) )
        self.pauzes = json.dumps(pauze)  
                 
    def end(self):
        if(not session['isPauzed'] == None):
            self.endPauze()
        if not self.start_date == None:
            self.end_date = datetime.utcnow()
        else:
            db.session.delete(self)
        db.session.commit()
        
    def setFeedback(self, score):
        self.feedback_score = score
        db.session.commit()
        
    @classmethod
    def getSessionByID(sessionID):
        return Session.query.filter_by(id = sessionID).first()
        
    def __repr__(self):
        return '<Session %r>' % self.title