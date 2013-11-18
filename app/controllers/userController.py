from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

from app import app
from app import db
from app.models.user import User
from werkzeug._internal import _log

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'userID' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first.')
            return redirect(url_for('login'))
    return wrap

def logout_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if not 'userID' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to logout first.')
            return redirect(url_for('home'))
    return wrap

@app.route('/home')
def home():
    return render_template('pages/dashboard.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('pages/dashboard.html')

@app.route('/user/login' , methods=['GET','POST'])
@logout_required
def login():
    error = None    
    if request.method == 'POST':
        if not isValidLogin(request.form['username'],request.form['password']):
            error = 'invalid username or password, please try again.'
        else:
            session['userID'] = User.query.filter_by(email= request.form['username']).first().id
            return redirect(url_for("welcome"))
    return render_template('pages/login.html' , error = error)
   

def isValidLogin( username, password):
    user = User.query.filter_by(email=username).first()
    if user == None or (not user.password == password):
        return False
    return True    

@app.route('/user/logout')
def logout():
    session.pop('userID',None)
    return redirect(url_for('login'))

@app.route('/user/register' , methods = ['GET','POST'])
@logout_required
def register():
    errors = {}
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        pass1 = request.form['pass1'] 
        pass2 = request.form['pass2']       
        if not isValidPass(pass1,pass2):
            error = 'The passwords you entered did not match'
            errors = errors + {"password" : error}
        if not isValidEmail:
            error = 'The email-address you entered is already taken'
            errors =  errors + {"email" : error}
        else:
            user = User(email, lastname, name, pass1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('pages/register.html' , errors = errors)


def isValidEmail(email):
    user = User.query.filter_by(email=username).first()
    if user == None:
        return True
    return False

def isValidPass(pass1 , pass2):
    return pass1 == pass2
