from app import app
from app import db
from datetime import datetime

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
    
    def endSession(self):
        self.end_date = datetime.utcnow()
    
    @staticmethod
    def hasRunningSession(userid):
        lastRunningSession = Session.query.filter_by(user_id = userid).order_by(Session.start_date).first()
        
        return lastRunningSession
        
        
    def __repr__(self):
        return '<Session %r>' % self.title