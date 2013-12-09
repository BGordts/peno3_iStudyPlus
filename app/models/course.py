from flask import *

from app import app
from app import db
from app.models.courseUsers import Courses_Users

from aifc import Error
from sqlalchemy.exc import IntegrityError

COURSES_1BACH_ING = ["analyse1" , "analyse2" , "algebra" , "algemene techniche scheikunde" , "mechanica 1" , "wijsbegeerte" ,
                    "toegepaste thermodynamica" , "materiaalkunde" ,"methodiek van de informatica" , "natuurkunde" , "elektrische netwerken"]

class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(500), unique=True)

    def __init__(self, course):
        self.course = course
        self.users = []

    def getAllUsers(self):
        users = []
        for i in Courses_Users.query.filter_by(course=self).all():
           users.append(i.user)
        return users 

    def addUserToCourse(self,user):
        association = Courses_Users(user,self)
        db.session.add(association)
        db.session.commit()
    
    @staticmethod    
    def addUserCoursesStudy(user, study):
        if( study == "1e Bach Burgerlijk Ingenieur"):
            for sub in COURSES_1BACH_ING:
                course = Course.query.filter_by(course=sub).first()
                course.addUserToCourse(user)
        db.session.commit()
                
    @staticmethod    
    def changeStudy(user, study):
        coursAssQuery = CourseUsers.query.filter_by(user=user)
        for associationCU in coursAssQuery:
            db.session.delete(associationCU)
        if( study == "1e Bach Burgerlijk Ingenieur"):
            for sub in COURSES_1BACH_ING:
                course = Course.query.filter_by(course=sub).first()
                course.addUserToCourse(user)
        db.session.commit()

    def deleteUser(self,user):
        self.users.remove(user)
        db.session.commit()

    @staticmethod
    def getAllCourses():
        return Course.query.all()

    def hasAsUser(self,user):
        if(user in self.getAllUsers()):
            return True
        return False

    def getCourseStatistic(self):
        return Courses_Users.query.filter_by(course=self).first().courseStatistic

def make_courses():
    try:
        for course in COURSES_1BACH_ING:
            nCourse = Course(course)
            db.session.add(nCourse)
        db.session.commit()
    except IntegrityError:
        pass