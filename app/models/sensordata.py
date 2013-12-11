from werkzeug._internal import _log

from app import app
from app import db
from app.utils.utils import *
import datetime

SENSOR_LIGHT = "light"
SENSOR_TEMPERATURE = "temperature"
SENSOR_HUMIDITY = "humidity"
SENSOR_SOUND = "sound"
SENSOR_CAMERA = "camera"
SENSOR_FOCUS = "focus"


class Sensordata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #sensorType light, temperature, humidity, camera
    sensor_type = db.Column(db.String(15))
    value = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    session_id = db.Column(db.Integer, db.ForeignKey('usersessions.id'))
    userSession = db.relationship('UserSession', backref=db.backref('sensordata', lazy='dynamic'))

    def __init__(self, sensor_type, userSession, value, date):
        self.sensor_type = sensor_type
        self.session_id = userSession.id
        self.value = value
        self.date = date      
        
    def output(self):
        timeInMilis = unix_time_millis(self.date)
        
        return  {"sensor_type": self.sensor_type, "value": self.value, "date": timeInMilis, "session_id": self.session_id}
    
    def outputXY(self):
        if self.sensor_type == SENSOR_FOCUS:
            if self.value == 0:
                return {"x": unix_time_millis(self.date), "y": None}
        
        return {"x": unix_time_millis(self.date), "y": self.value}

    def __repr__(self):
        return '<Sensordata %r>' % self.sensor_type