import json

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from userController import login_required

from app import app
from app import db

from app.models.course import Course
from app.models.user import User

from werkzeug._internal import _log
from werkzeug import secure_filename

@app.route('/statistics/getGeneralUserStatistics')
def getGeneralUserStatistics():
    userID = request.args["userID"]
    
    user = User.query.get(userID)
    
    return json.dumps(user.statistic.outputData())