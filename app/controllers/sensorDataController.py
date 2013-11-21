from flask.ext.sqlalchemy import SQLAlchemy
import datetime

from app import app
from app import db

from app.models.sensordata import Sensordata
from app.models.session import Session
from app.models.user import User
   
@app.route('/sensorData/postSensorData', methods = ['GET','POST']) 
def postSensorData():
    #What the client sends to us
    userID = request.form["userID"]
    sensor_type = request.form["sensortype"]
    value = request.form["value"]
    #Date in miliseconds
    dateInMilis = request.form["date"]
    
    user = User.getUserByID(userID)
    session = user.getRunningSession()
    
    date = datetime.datetime.fromtimestamp(dateInMilis/1000.0)
    
    #Check whether the user has a running session
    if session:
        sensorData = SensorData(sensor_type, session, value, date)
    
        db.session.add(sensorData)
        db.session.commit()
    #If the user has no running session, just do nothing
        
    return ""
    