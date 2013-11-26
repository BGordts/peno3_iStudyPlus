from app import app
from app import db
from datetime import datetime

class Sensordata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #sensorType light, temperature, humidity, camera
    sensor_type = db.Column(db.String(15))
    value = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    session = db.relationship('Session', backref=db.backref('sensordata', lazy='dynamic'))

    def __init__(self, sensor_type, session, value, date):
        self.sensor_type = sensor_type
        self.session_id = session.id
        self.value = value
        self.date = date        

    def __repr__(self):
        return '<Sensordata %r>' % self.sensor_type