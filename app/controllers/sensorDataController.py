from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db

from app.models.sensordata import Sensordata
from app.models.session import Session
from app.models.user import User
   
   '''
@app.route('/sensorData/postSensorData') 
def postSensorData():
    #What the client sends to us
    userID = request.form["userID"]
    sensor_type = request.form["sensortype"]
    value = request.form["value"]
    
    user = User.getUserByID(userID)
    session = user.getRunningSession()
    
    #Check whether the user has a running session
    if session:
        sensorData = SensorData(sensor_type, session, value)
    
        db.session.add(sensorData)
        db.session.commit()
    #If the user has no running session, just do nothing
        
    return ""

@app.route('/sensorData/registerDevice') 
def registerDevice():
    device_key = request.form["devicekey"]
    '''
    