from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

from app import app
from app import db
from app.models.user import User
from werkzeug._internal import _log
# from app.forms.loginForm import LoginForm

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'userID' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/home')
def home():
    return render_template('pages/dashboard.html')

@app.route('/welcome')
@login_required
def welcome():
    return 'dit is de welkom-pagina, na inloggen'

@app.route('/user/login' , methods=['GET','POST'])
def login():
    error = None    
    if request.method == 'POST':
        if not isValidLogin(request.form['username'],request.form['password']):
            error = 'invalid username or password, please try again.'
        elif 'userID' in session:
            error = "log out first"
        else:
            session['userID'] = User.query.filter_by(email= request.form['username']).first().getID()
            return redirect(url_for("welcome"))
    return render_template('pages/login.html' , error = error)
   

def isValidLogin(username, password):
    user = User.query.filter_by(email=username).first()
    if user == None or (not user.password == password):
        return False
    return True

@app.route('/user/logout')
def logout():
    session.pop('userID',None)
    return redirect(url_for('login'))

@app.route('/user/register' , methods = ['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        _log('info',request.form['email'] )
        _log('info',request.form['name'] )
        _log('info',request.form['lastname'] )
        _log('info',request.form['pass1'] )
        email = request.form['email']
        name = request.form['name']
        lastname = request.form['lastname']
        password = request.form['pass1']
        
        if False:
            error = 'some of the data you entered was invalid, please check again.'
        else:
            _log('info', "test")
            user = User(email, lastname, name, password)
            db.session.add(user)
            db.session.commit()
            error = 'You were successfully registered and can login now'
            _log('info', error)
            return redirect(url_for('login'))
    return render_template('pages/register.html' , error = error)

if __name__ == '__main__':
    app.run()
