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
        
    
    def startSession(self):
        self.start_date = datetime.utcnow()
        while not self.isSessionEnded():
            self.updateValues()
            
    def isSessionEnded(self):
        return self.end_date == None
    
    def updateValues(self):
        "steekt de waardes van de arduino in de gepaste lijst van dit object"
        pass

    
    def endSession(self):
        "commit de session in de db"
        self.end_date = datetime.utcnow()
        
    @classmethod
    def getSessionByID(sessionID):
        return User.query.filter_by(id = sessionID).first()
    
    '''
    Classmethod to check wheter the given User has a running session or not.
    '''
    @staticmethod
    def hasRunningSession(user):
        lastRunningSession = user.sessions.order_by(Session.start_date).first()
        return True if lastRunningSession.end_date else False        
        
    def __repr__(self):
        return '<Session %r>' % self.title