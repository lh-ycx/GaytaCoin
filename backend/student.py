# -*- coding: UTF-8 -*-
import json
import random
import copy
from flask_pymongo import PyMongo
class Student_Manager(object):
    def __init__(self,db):
        self.db = db

        # 前后端交互用的是openid, openid 转成的id是MongoDB中标识唯一行的id
        self.openid2id = {}
    
    def getStudentbyopenid(self,openid):
        res = self.db.Student.find_one({"openid":openid})
        if res is not None:
            return json.dumps({'response_code':1,"stuName":res['stuName'],"stuId":res['stuId']})
        print('error: openid ',openid,' does not exist!')
        return json.dumps({'response_code':0})
    
    def getRegisterListbyopenid(self,openid):
        res = []
        cursor = self.db.Register.find({"openid":openid})
        if cursor is None:
            return res
        
        dic = {"registerId":[],"openid":[],"courseId":[],"timestamp":[]}
        
        for c in cursor:
            dic['registerId'] = c['registerId']
            dic['openid'] = c['openid']
            dic['courseId'] = c['courseId']
            dic['timestamp'] = c['timestamp'] 
            res.append(copy.deepcopy(dic))
        return res

    def addStudent(self,openid,stuId,stuName):

        res = self.db.Student.find_one({"openid":openid})
        if res is not None:
            return False

        self.db.Student.insert_one({"openid":openid,"stuId":stuId,"stuName":stuName}).inserted_id

        return True
    
    def printStudents(self): 
        cursor = self.db.Student.find({})
        for stu in cursor:
            print("===============================Student ",stu["_id"]," ==========================")
            print("openid: ",stu['openid'])
            print("stuId: ",stu['stuId'])
            print("stuName: ",stu['stuName'])

    def getopenid(self,openid):
        res = self.db.Student.find_one({'openid':openid})
        if res is not None:
            return res['openid']
        return False
    
    def getstuId(self,openid):
        res = self.db.Student.find_one({'openid':openid})
        if res is not None:
            return res['stuId']
        return False
    
    def getstuName(self,openid):
        res = self.db.Student.find_one({'openid':openid})
        if res is not None:
            return res['stuName']
        return False
    
    def register(self,openid,courseId,timestamp):
        
        #首先查找学生是否存在
        res = self.db.Student.find_one({"openid":openid})
        if res is None:
            return -2
        
        #然后查找课程是否存在
        res = self.db.Courses.find_one({"courseId":courseId})
        if res is None:
            return -1

        cursor = self.db.Register.find({})
        lis = []
        for c in cursor:
            lis.append (c['registerId'])

        if lis:
            registerId = max(lis) + 1
        else:
            registerId = 1
        self.db.Register.insert_one({"registerId":registerId,"openid":openid,"courseId":courseId,"timestamp":timestamp})
        return 1

    def getCoursesByOpenid(self,openid):

        res = self.db.Register.find({"openid":openid})
        # 没有签过到
        if res is None:
            return json.dumps({"response_code":0})
        
        lis = []
        course_list = []
        temp = {"courseId":-1,"courseName":""}
        for record in res:
            if record['courseId'] not in course_list:
                 course_list.append(copy.deepcopy(record['courseId']))

        for id in course_list:
            temp["courseId"] = id
            temp["courseName"] = self.db.Courses.find_one({"courseId":id})['courseName']
            lis.append(copy.deepcopy(temp))
        return json.dumps([{"response_code":1},lis])

