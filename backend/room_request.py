# -*- coding: UTF-8 -*-
import datetime
# from usr import Usr


class Room_request(object):
    def __init__(self):
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.name = ""
        #self.subarea = ""
        #self.description = ""
        self.courseId = -1

    def getTime(self):
        return self.time

    def getName(self):
        return self.name

    def getCourseId(self):
        return self.courseId

    def setTime(self):
        # 将时间更改为当前时间，总是返回True
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return True

    def setName(self, name):
        # if isinstance(name, str):
        self.name = name
        return True
        # print("error: ", name, " is not a string!")
        # return False

    def setCourseId(self, courseId):
        self.courseId = courseId

    def checkReq(self):
        # 查看该request实例是否满足创建房间的需求
        if not isinstance(self.name, str) or self.name == "":
            print("error: check room name failed!")
            return False
        if self.courseId < 0:
            print("error: check courseId failed!")
            return False
        return True
