import json
from collections import OrderedDict

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db

from app.models.userSession import UserSession
from app.models.course import Course
from app.models.user import User
from app.models.generalUser import GeneralUser
from werkzeug._internal import _log

'''
Returns the general user statistics for the requested users
'''
@app.route('/statistics/getGeneralUserStatistics')
def getGeneralUserStatistics():
    userID1 = request.args["userID1"]
    userID2 = request.args["userID2"]
    
    returndict = {}
    
    user1 = User.query.get(userID1)
    returndict["user1"] =  user1.statistics.outputData()
    
    user2 = None
    _log("info", "lolo: " + userID2)
    if int(userID2) != -1:
        user2 = User.query.get(userID2)
        returndict["user2"] = user2.statistics.outputData()
    
    return json.dumps(returndict)

@app.route('/statistics/getGeneralUserStatistics2')
def getGeneralUserStatistics2():
    returndict = {}
    genUser = GeneralUser.query.first()
    returndict["genUser"] = genUser.statistics.outputData()
    
    return json.dumps(returndict)

'''
@app.route('/statistics/getCourseStatistics')
def getCourseStatistics():
    userID1 = request.args["userID1"]
    courseID = request.args[""]
        
    returndict = {}
    
    user1 = User.query.get(userID1)
    returndict["user1"] =  user1.statistics.outputData()
    
    user2 = None
    _log("info", "lolo: " + userID2)
    if int(userID2) != -1:
        user2 = User.query.get(userID2)
        returndict["user2"] = user2.statistics.outputData()
    
    return json.dumps(returndict)
'''

'''
Looks at all the sessions and returns the conbination of sensor average for a session and the efficiency of that session
'''
@app.route('/statistics/getEfficiencyForSensor', methods = ['GET'])   
def getEfficiencyForSensor():
    userID1 = request.args["userID1"]
    userID2 = request.args["userID2"]    
    courseID = request.args["courseID"]    
    sensor_type = request.args["sensor_type"]
    
    returnMap = {}
    
    if userID2 == int(-1):
        returnMap = {'1': helper(userID1, sensor_type, courseID), '2': {}}
    else:
        returnMap = {'1': helper(userID1, sensor_type, courseID), '2': helper(userID2, sensor_type, courseID)}
    
    return json.dumps(returnMap)

def helper(userID, sensor_type, courseID):        
    user = User.query.get(userID)
    
    sessions = []
    
    if int(courseID) == -1:
        sessions = UserSession.query.filter_by(user = user).all()
    else:
        sessions = UserSession.query.filter_by(course_id = courseID).filter_by(user = user).all()
    
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
    
    return returnMap