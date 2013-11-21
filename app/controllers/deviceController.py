from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
from werkzeug._internal import _log

from app import app
from app import db

from app.models.device import Device
from app.models.user import User
   
@app.route('/device/register', methods = ['GET']) 
def registerDevice():
    _log('info', 'device key:' + request.args["kut"])
    _log('info', 'device key:' + request.args.__repr__())
    device_key = request.form["devicekey"]
    
    _log('info', 'device key: ' + device_key)
    
    user_id = session["userID"]
    
    #Save the device
    device = Device(device_key, User.getUserByID(user_id))
    db.session.add(device)
    db.session.commit()

    return "lol"