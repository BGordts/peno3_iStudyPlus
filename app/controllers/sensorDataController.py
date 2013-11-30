from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug._internal import _log

import datetime

from app import app
from app import db

from app.models.sensordata import Sensordata
from app.models.userSession import UserSession
from app.models.user import User
from app.models.device import Device
   
'''
The pi device sends his recorded sensor data to this url to store it in the database
'''

@app.route('/sensorData/postSensorData', methods = ['GET']) 
def postSensorData():
    #What the client sends to us
    device_key = request.args["deviceKey"]
    sensor_type = request.args["sensortype"]
    value = request.args["value"]
    #Date in miliseconds
    dateInMilis = float(request.args["date"])
    
    device = Device.getDeviceByKey(device_key)
    _log('info', "device: " + device.__repr__())
    user = Device.getDeviceByKey(device_key).getUser()
    _log('info', "user: " + user.__repr__())
    session = user.getRunningSession()
    _log('info', "session: " + session.__repr__())
    
    date = datetime.datetime.fromtimestamp(dateInMilis/1000.0)
    _log('info', "date: " + date.__repr__())
    
    #Check whether the user has a running session
    if session:
        if not session.isPaused():            
            sensorData = Sensordata(sensor_type, session, value, date)
        
            db.session.add(sensorData)
            db.session.commit()
            
            return "Sensordata saved"
        else:
            return "Session is paused"
    else:
        return "There is no running session at the moment"
    #If the user has no running session, just do nothing