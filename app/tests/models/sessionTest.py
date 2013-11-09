'''
Created on 7-nov.-2013

@author: Boris
'''
import unittest
from app import app
from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from app.models.user import User

# http://flask.pocoo.org/mailinglist/archive/2012/10/7/how-to-properly-test-a-python-flask-system-based-on-sqlalchemy-declarative/#2f21ffac721711aae03207b078e4e9d3
class MyTest(unittest.TestCase):
    
    def setUp(self):
        """Before each test, set up a blank database"""
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        #Drop the database
        db.drop_all()
        db.create_all()
        
    def tearDown(self):
        #Drop the database
        db.drop_all()
        db.create_all()
        
    def test_lol(self):       
        admin = User('admin@example.com', 'admin', 'adminus', 'kaka')
        guest = User('b@a.be', 'kaka', 'pipi', 'kaka')
        
        db.session.add(admin)
        db.session.add(guest)
        db.session.commit()
        
        print User.query.all()
        

    if __name__ == '__main__':
        unittest.main()