'''
Created on 6-nov.-2013

@author: Boris
'''
from app import app

@app.route('/')
def hello_world():
    return 'Hello World hallloooo'