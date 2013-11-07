'''
Created on 6-nov.-2013

@author: Boris
'''
from app import app

@app.route('/')
def hello_world():
    return 'Hello World hallloooo oo oo oo'

@app.route('/user/login')
def login():
    return "log in"

@app.route('/user/logout')
def logout():
    return "log out"

@app.route('/user/register')
def register():
    return "log register"