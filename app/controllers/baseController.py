from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

from app import app
from app import db

from app.models.user import User

@app.route('/home')
def home():
    user = User.query.get(session["userID"])
    return render_template('pages/dashboard_profile-info2.html', user=user)

@app.route('/vakken')
def dbord():
    user = User.query.get(session["userID"])
    return render_template('pages/coursesview.html', user=user)

@app.route('/welcome')
def welcome():
    return render_template('pages/dashboard.html')

@app.route('/app/<path:path>')
@app.route('/app')
def angularRoutes(path=None):
    return render_template('pages/dashboard_profile-info.html')