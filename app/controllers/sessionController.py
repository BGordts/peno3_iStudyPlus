'''
Created on 7-nov.-2013

@author: Boris
'''
from app import app

@app.route('/session/create')
def create():
    print "create"
