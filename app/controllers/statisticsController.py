import json
from collections import OrderedDict

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from userController import login_required

from app import app
from app import db

from app.models.userSession import UserSession
from app.models.course import Course
from app.models.user import User

from werkzeug._internal import _log

@app.route('/statistics/getGeneralUserStatistics')
def getGeneralUserStatistics():
    userID = request.args["userID"]
    
    user = User.query.get(userID)
    
    return json.dumps(user.statistics.outputData())

'''
Looks at all the sessions and returns the conbination of sensor average for a session and the efficiency of that session
'''
@app.route('/statistics/getEfficiencyForSensor', methods = ['GET'])   
def getEfficiencyForSensor():
    userID = request.args["userID"]
    sensor_type = request.args["sensor_type"]
    
    user = User.query.get(userID)
    
    sessions = UserSession.query.filter_by(user = user).all()
    
    returnMap = {}
    
    for nextSession in sessions:
        sensorValue = 0
        efficiency = nextSession.sessionEff
        
        if sensor_type == "illumination":
            sensorValue = nextSession.sessionIll
        elif sensor_type == "temperature":
            sensorValue = nextSession.sessionTemp
        elif sensor_type == "humidity":
            sensorValue = nextSession.sessionHum
        elif sensor_type == "sound":
            sensorValue = nextSession.sessionSound
        elif sensor_type == "focus":
            sensorValue = nextSession.sessionFocus
        else:
            return "Incorrect sensor value"
        
        returnMap[sensorValue] = efficiency
    
    #Sort the dictionary by key
    OrderedDict(sorted(returnMap.items(), key=lambda t: t[0]))
    
    return json.dumps(returnMap)