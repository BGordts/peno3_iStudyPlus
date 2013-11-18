from flask.ext.sqlalchemy import SQLAlchemy

from app import app
from app import db

from app.models.sensordata import Sensordata
from app.models.session import Session
   
@app.route('/sensorData/postSensorData') 
def postSensorData():
    userID = request.form["userID"]
    #sensortypes: light, temperature, sound, humidity, webcam
    sensor_type = request.form["sensortype"]
    value = request.form["value"]
    
    #Check if 
    
    sensorData = SensorData(sensor_type, Session.getSessionByID(sessionID), value)
    
    db.session.add(sensorData)
    db.session.commit()