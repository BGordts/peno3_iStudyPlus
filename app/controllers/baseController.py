from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

from app import app
from app import db

from app.models.user import User

@app.route('/')
def welcome():
    try:
        user = User.query.get(session["userID"])
        return render_template('pages/dashboard_profile-info2.html', user=user)
    except KeyError:
        return render_template('index.html')
    
@app.route('/home') 
def home():
    try:
        user = User.query.get(session["userID"])
        return render_template('pages/dashboard_profile-info2.html', user=user)
    except KeyError:
        return redirect(url_for('login'))

@app.route('/app/<path:path>')
@app.route('/app')
def angularRoutes(path=None):
    return render_template('pages/dashboard_profile-info.html')