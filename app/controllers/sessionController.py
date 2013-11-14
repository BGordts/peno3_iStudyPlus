'''
Created on 7-nov.-2013

@author: Boris
'''
from app import app
from app.models.user import User
from app.models.session import Session

@app.route('/session/create')
def create():
    print "create"
  
@app.route('/session/isSessionRunning')  
def isSessionRunning():
    u = User.getAdminUser()
    s = Session.hasRunningSession(u.id)
    
    return s.__str__()