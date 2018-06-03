# -*- coding: UTF-8 -*-
import json
import random
import copy
from flask_pymongo import PyMongo
class Teacher_Manager(object):
    def __init__(self,db):
        self.db = db

        # 前后端交互用的是teacherId,转成的id是MongoDB中标识唯一行的id
        self.teacherId2id = {}
    
    def getTeacherbyteacherid(self,teacherId):
        res = self.db.Teacher.find_one({"teacherId":teacherId})
        if res is not None:
            return json.dumps({'response_code':1,"teacherId":res["teacherId"],"teacherName":res["teacherName"],"courses":res["courses"]})
        print('error: teacherId ',teacherId,' does not exist!')
        return json.dumps({'response_code':0})
    
    def addTeacher(self,teacherId,password,teacherName):

        res = self.db.Teacher.find_one({"teacherId":teacherId})
        if res is not None:
            return False
        
        self.teacherId2id = Teacher.insert_one({"teacherId":teacherId,"password":password,"teacherName":teacherName}).inserted_id

        return True
    
    def printTeachers(self): 
        cursor = self.db.Teacher.find({})
        for t in cursor:
            print("===============================Teacher ",t["_id"]," ==========================")
            print("teacherId: ",t['teacherId'])
            print("password: ",t['password'])
            print("teacherName: ",t['teacherName'])
            print("courses",t['courses'])

    def getteacherId(self,teacherId):
        res = self.db.Teacher.find_one({'teacherId':teacherId})
        if res is not None:
            return res['teacherId']
        return False
    
    def getteacherName(self,teacherId):
        res = self.db.Teacher.find_one({'teacherId':teacherId})
        if res is not None:
            return res['teacherName']
        return False
    
    def getteacherCourses(self,teacherId):
        res = self.db.Teacher.find_one({'teacherId':teacherId})
        if res is not None:
            return res['courses']
        return False

    def resetPassword(self,teacherId,new_password,old_password):
        res = self.db.Teacher.find_one({'teacherId':teacherId})
        if res is None:
            print("error: teacher",teacherId," does not exist!")
            return json.dumps({"response_code":-1})
        
        if old_password == res['password'] :
            self.db.Teacher.update({'teacherId':teacherId},{"$set":{'password':new_password}})
            return json.dumps({"response_code":1})
        
        return json.dumps({"response_code":0})
    

    def addCourse(self,teacherId,course_name):
        res = self.db.Teacher.find_one({'teacherId':teacherId})['courses']
        if res is None:
            print("error: teacher", teacherId," does not exist!")
            return json.dumps({"response_code":-1})

        ll = self.db.Courses.find_one({'courseName':course_name})
        if ll is not None:
            print("error Course ",course_name," already exists")
            return json.dumps({"response_code":0})
        #首先更新Teacher表
        
        lis = copy.deepcopy(res)
        lis.append (course_name)
        print (lis)
        self.db.Teacher.update({'teacherId':teacherId},{"$set":{'courses': lis}})
        
        #然后更新Courses表
        c_Id=[]
        cursor = self.db.Courses.find({})
        for c in cursor:
            c_Id.append(c['courseId'])
        
        #生成课程编号
        candidateId = max(c_Id) + 1 
        self.db.Courses.insert_one({"courseName":course_name,"courseId":candidateId,"teacherId":teacherId})
        return json.dumps({"response_code":1})

    def deleteCourseByName(self,teacherId,course_name):
        res = self.db.Teacher.find_one({'teacherId':teacherId})['courses']
        if res is None:
            print("error: teacher", teacherId," does not exist!")
            return False
        if course_name not in res:
            print("error: course ",course_name," does not exist!")
            return False
        

        #首先更新Teacher表
        self.db.Teacher.update({'teacherId':teacherId},{"$set":{'courses':res.remove(course_name)}})
        
        #然后更新Courses表
        self.db.Courses.delete_one({'courseName':course_name})
        return True

    def deleteCourseById(self,teacherId,courseId):
        res = self.db.Courses.find_one({'courseId':courseId})
        if res is None:
            print("error: course ",courseId," does not exists!" )
            return False
        
        teacherId = res ['teacherId']
        courseName = res ['courseName']
        #首先更新Courses表
        self.db.Courses.delete_one({'courseId':courseId})

        #然后更新Teacher表
        res = self.db.Teacher.find_one({'teacherId':teacherId})['courses']
        if res is None:
            print("error: teacher", teacherId," does not exist!")
            return False

        lis = copy.deepcopy(res)
        lis.remove(courseName)
        self.db.Teacher.update({'teacherId':teacherId},{"$set":{'courses':lis}})
        return True
        
    def checkPassword(self,teacherId,password):
        res = self.db.Teacher.find_one({'teacherId':teacherId})['password']
        if res is None:
            print("error: teacher ",teacherId," does not exist!")
            return False
        if res == password:
            return True
        return False
    
    def getRegisterListbyCourseId(self,courseId):
        res = self.db.Register.find({"courseId":courseId}).sort({"registerId":1})
        dic = {"openid":[],"courseId":[],"timestamp":[]}
        lis = []
        for c in res:
            dic["openid"] = c["openid"]
            dic["courseId"] = c["courseId"]
            dic["timestamp"] = c["timestamp"]
            lis.append(dic)

        return lis
