import json
from flask_pymongo import PyMongo
class Course_Manager(object):
    def __init__(self,db):
        self.db = db
    
    def getCourseName(self,courseId):
        if self.db.Courses:
            res = self.db.Courses.find_one({"courseId":courseId})['courseName']
            if res is None:
                return False
            return res
        else:
            return False 
    def getCourseId(self,courseName):
        if self.db.Courses:
            res = self.db.Courses.find_one({"courseName":courseName})['courseId']
            if res is  None:
                return False
            return res
        else:
            return False
