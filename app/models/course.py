from flask import *

from app import app
from app import db

from app.models.session import Session


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(120), unique=True)
    
    def __init__(self, course):
        self.course = course
    
    def getAllUser(self, course):
        pass
    
    @staticmethod
    def getAllCourses():
        courses= []
        for course in Course.query.all():
            courses.append(course.course)
        return courses
    
    "blebleboris"
        
        
    
    