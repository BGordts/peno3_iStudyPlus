from flask import *
from functools import wraps

from app import app
from app import db
from app.models.user import User
from werkzeug._internal import _log
from app.forms.loginForm import LoginForm

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
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

@app.route('/login' , methods=['GET','POST'])
def login():
    error = None    
    if request.method == 'POST':
        if not request.form["username"] == "admin" and False:
        #if not isValidLogin(request.form['username'],request.form['password']):
            error = 'invalid username or password, please try again.'
        else:
            #session['user'] = User.query.filter_by(email= username).first()
            return redirect(url_for("welcome"))
    return render_template('pages/login.html' , error = error)
   

def isValidLogin( username, password):
    user = User.query.filter_by(username= username).first()
    if user == None or user.getPass != password:
        return False
    return True    

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login.html'))

@app.route('/register' , methods = ['GET','POST'])
def register():
    error = None
    email = request.form['email']
    name = request.form['name']
    lastname = request.form['lastname']
    password = request.form['password']
    if email == None or name == None or lastname == None or password == None:
        error = 'some of the data you entered was invalid, please check again.'
    else:
        user = User(email, lastname, name, password)
        db.session.add(user)
        db.session.commit()
        flash('You were successfully registered and can login now')
        return redirect(url_for('login'))
    return render_template('register.html' , error = error)

if __name__ == '__main__':
    app.run()
