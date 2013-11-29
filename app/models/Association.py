from flask import *

from app import app
from app import db

from app.models.statistics import Statistic

class Courses_Users(db.Model):
    __tablename__ = 'Courses_Users'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') , primary_key=True)
    user = db.relationship("User")
    
    course_id = db.Column(db.Integer, db.ForeignKey('course.id') , primary_key=True)
    course = db.relationship("Course")
    
    courseStastic_id = db.Column(db.Integer, db.ForeignKey('statistic.id'))
    courseStatistic = db.relationship('Statistic', backref=db.backref('Association', lazy='dynamic'))

    def __init__(self,user,course):
        self.user = user
        self.course = course
        courseStatistics = Statistic()
        self.courseStatistic = courseStatistics
        