from app import app
   
@app.route('/session/postSensorData') 
def postSensorData():
    sessionID = request.form["sessionID"]
    #sensortypes: light, temperature, sound, humidity, webcam
    sensortype = request.form["sensortype"]