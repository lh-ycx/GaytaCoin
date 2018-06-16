# -*- coding: UTF-8 -*-
from room_request import Room_request
from flask_pymongo import  PyMongo
import datetime
import json
from bson.json_util import dumps
'''
         数据库表 Room 结构如下
        {
            "_id" : ObjectId("    "),
            "room_id": 3,    (这里的room_id其实就是courseId,每个课程只有一个群)
            "name"： "LOL" ,(指定为课程名，群名即课程名)
            "users":[
                "1500012863",
                "1500012758"
            ],  (users是所有群里的学生的stuId)
            "owner":"21321", (owner 是课程的老师的teacherId)
            "messages": [
                {
                    "user": "1500012863", (stuId)
                    "content":"约吗？",
                    "time": 
                },
                {
                    "user":,
                    "content":,
                    "time":
                }
            ] (这是所有的聊天记录)
        }
'''
class Room_manager(object):
    def __init__(self, db):
        self.db = db
        self.rooms = []

    def getRoombyroomid(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            return dumps({"response_code": 0})

        for i,stuId in enumerate(res['users']):
            res['users'][i] = self.db.Student.find_one({"stuId":stuId})
        
        res['owner'] = self.db.Teacher.find_one({"teacherId":res['owner']})
        
        for i in range(len(res['messages'])):
            res['messages'][i]['user'] = self.db.Student.find_one({"openid":res['messages'][i]['user']})

        return dumps([{"response_code": 1}, res])

    def joinRoom(self, stuId, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code": 0})
        self.db.Room.update_one({"room_id": room_id}, {
                                "$addToSet": {"users": stuId}})
        return dumps({"response_code": 1})

    def deleteRoom(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code": 0})
        self.db.Room.delete_one({"room_id": room_id})
        return dumps({"response_code": 1})

    def deleteByID(self, room_id, stuId):
        res = self.db.Room.update_one({"room_id": (room_id)}, {
                                      "$pull": {"users": stuId}})
        if res.matched_count == 0:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code": 0})
        return dumps({"response_code": 1})

    def addRoombyreq(self, request):
        #根据request创建房间，成功返回房间id，失败返回False
        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            return dumps({"response_code": 0})
        room = self.db.Room
        room.insert_one({"room_id": request.courseId, "name": request.getName(), "owner": request.getRoom_owner(),
                         "users": [request.getRoom_owner()], "messages": []})
        # self._id += 1
        return dumps({"response_code": 1, "room_id": courseId})

    def searchRoom(self, request):
        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            return dumps({"response_code": 0})

        room = self.db.Room
        query = {}
        if request.getName() != "":
            query['name'] = request.getName()
        res = room.find(query)

        cur = [x for x in res]
        for k, room in enumerate(cur):
            cur[k]['owner'] = self.db.Teacher.find_one(
                {"teacherId": room['owner']})
            for i, stuId in enumerate(room['users']):
                room['users'][i] = self.db.Student.find_one({"stuId": stuId})

        return dumps([{"response_code": int(res.count() != 0)}, cur])

    def getName(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['name']

    # 该函数用于查找指定teacherId的老师所开课程的房间
    def getRoomByOwnID(self, teacherId):
        cur = self.db.Room.find({"owner": teacherId})
        if cur.count() == 0:
            return dumps({"response_code":1})

        cur = list(cur)
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.Teacher.find_one({"teacherId":room['owner']})
            for i,stuId in enumerate(room['users']):
                room['users'][i] = self.db.Student.find_one({"stuId":stuId})

        return dumps([{"response_code":1},list(cur)])

    # 该函数用于查找指定stuId的同学参加的课程的房间
    def getRoomByStuID(self, stuId):
        cur = self.db.Room.find({"users": stuId})
        if cur.count() == 0:
            return dumps({"response_code":1})

        cur = list(cur)
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.Teacher.find_one({"teacherId":room['owner']})
            for i,stuId in enumerate(room['users']):
                room['users'][i] = self.db.Student.find_one({"stuId":stuId})

        return dumps([{"response_code":1},list(cur)])

    # 该函数用于返回指定courseId的课程房间
    def getRoomByCourseId(self, courseId):
        cur = self.db.Room.find({"room_id":courseId})
        if cur.count() == 0:
            return dumps({"response_code":0})
        cur = list(cur)
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.Teacher.find_one({"teacherId":room['owner']})
            for i,stuId in enumerate(room['users']):
                room['users'][i] = self.db.Student.find_one({"stuId":stuId})        
        return dumps([{"response_code":1},list(cur)])

    def getRoom_owner(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['owner']

    def getUsrs(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['users']

    def setName(self, room_id, name):
        res = self.db.Room.update_one({"room_id": room_id},{"$set":{"name":name}})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True

    def addUsr(self, room_id, stuId):
        old_usr = self.db.Room.find_one({"room_id":room_id})['users']
        res = self.db.Room.update_one({"room_id": room_id}, {"users": old_usr + usrid})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True

    def setRoomOwner(self, room_id, teacherId):
        # old_usr = self.db.Room.find_one({"room_id": room_id})['owner']
        res = self.db.Room.update_one({"room_id": room_id}, {"$set":{"owner": teacherId}})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True

    def setRoomUsers(self, room_id, usrs):
        # old_usr = self.db.Room.find_one({"room_id": room_id})['owner']
        res = self.db.Room.update_one({"room_id": room_id}, {"$set":{"users": usrs}})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True

    def addMessageByStudent(self,room_id,openid,content):
        entry = {"user":openid,"content":content,"time":datetime.datetime.utcnow()}
        print(entry)
        res = self.db.Room.update_one({"room_id": room_id}, {"$push": {"messages":entry}})
        if res.matched_count is 0:
            print("error: room ", room_id, " or ", openid," does not exist!")
            return dumps({"response_code": 0})
        return dumps({"response_code": 1})

    def getMessage(self,room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code":0})
        if len(res['messages']) == 0:
            return dumps({"response_code": 0})
        return dumps([{"response_code": 1},res['messages']])

    def clearMessage(self,room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code":0})
        if len(res['messages']) == 0:
            return dumps({"response_code": 0})
        res = self.db.Room.update_one({"room_id": room_id}, {"$set":{"messages":[]}})
        return dumps({"response_code": 1})
