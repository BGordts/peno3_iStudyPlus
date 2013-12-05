from flask import *

from app import app
from app import db

class Courses_Users(db.Model):
    __tablename__ = 'Courses_Users'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , primary_key=True)
    user = db.relationship("User")
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id') , primary_key=True)
    course = db.relationship("Course")
    
    courseStastics_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    courseStatistics = db.relationship('Statistics', backref=db.backref('Courses_Users', lazy='dynamic'))

    def __init__(self,user,course):
        self.user = user
        self.course = course
        from app.models.statistics import Statistics
        courseStatistics = Statistics()
        self.courseStatistics = courseStatistics
        