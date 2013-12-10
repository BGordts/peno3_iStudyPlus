from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug._internal import _log

import datetime
import json

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
    
    #Check if there is a device found
    if device:
        _log('info', "device: " + device.__repr__())
        user = Device.getDeviceByKey(device_key).getUser()
        _log('info', "user: " + user.__repr__())
        userSession = user.getRunningSession()
        _log('info', "userSession: " + userSession.__repr__())
        
        date = datetime.datetime.fromtimestamp(dateInMilis/1000.0)
        _log('info', "date: " + date.__repr__())
        
        #Check whether the user has a running session
        if userSession:
            if not userSession.isPaused():            
                sensorData = Sensordata(sensor_type, userSession, int(value), date)
            
                db.session.add(sensorData)
                db.session.commit()
                
                return "Sensordata saved"
            else:
                return "Session is paused"
        else:
            return "There is no running session at the moment"
    else:
        return "There is no device registered with key " + device_key
    
@app.route('/sensorData/getSensordataForSession', methods = ['GET']) 
def getSensordataForSession():
    sessionID = request.args["sessionID"]
    
    session = UserSession.query.get(sessionID)
    
    returndict = {}
    
    returndict["illumination"] = session.outputSensorDataXY("illumination")
    returndict["temperature"] = session.outputSensorDataXY("temperature")
    returndict["humidity"] = session.outputSensorDataXY("humidity")
    returndict["sound"] = session.outputSensorDataXY("sound")
    returndict["focus"] = session.outputSensorDataXY("focus")
    
    return json.dumps(returndict)
    
    