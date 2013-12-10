from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

from app import app
from app import db

from app.models.user import User

from app.controllers.filters import login_required
from app.controllers.filters import logout_required
from app.controllers.filters import session_required
from app.controllers.filters import endSession_required

@app.route('/')
def welcome():
    try:
        user = User.query.get(session["userID"])
        return redirect("app/" + user.id.__str__() + "/dashboard")
        #return render_template('pages/dashboard_profile-info2.html', user=user)
    except KeyError:
        return render_template('index.html')
    
'''
TO REMOVE
'''
@app.route('/home') 
def home():
    try:
        user = User.query.get(session["userID"])
        return redirect("app/" + user.id + "/dashboard")
        #return render_template('pages/dashboard_profile-info2.html', user=user)
    except KeyError:
        return redirect(url_for('login'))
    
@app.route('/app/<path:path>')
@app.route('/app')
@login_required
@endSession_required
def angularRoutes(path=None):
    return render_template('pages/dashboard_profile-info.html')