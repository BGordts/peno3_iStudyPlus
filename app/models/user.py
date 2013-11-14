from app import app
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80), unique=False)
    surname = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(30), unique=False)

    def __init__(self, email, name, surname, password):
        self.email = email
        self.name = name
        self.surname = surname
        self.password = password    
    
    @staticmethod
    def getAdminUser():
        return User.query.filter_by(id = 1).first()   
    
    def __repr__(self):
        return '<User %r>' % self.email