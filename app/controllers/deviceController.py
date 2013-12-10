from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
from werkzeug._internal import _log

from app import app
from app import db

from app.models.device import Device
from app.models.user import User
   
'''
Method to link a pi and its user. Can also be used to change the device
'''
@app.route('/device/register', methods = ['GET']) 
def registerDevice():
    device_key = request.args["devicekey"]
        
    user = User.getUserByID(session["userID"])
    device = user.getDevice()
    if(device):
        device.key = device_key
    else:
        device = Device(device_key, user)
        db.session.add(device)
    
    #Save the device
    db.session.commit()

    return "ok"