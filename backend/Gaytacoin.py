# -*- coding: UTF-8 -*-

import hashlib
import json,yaml
import decimal
import requests
import copy
from textwrap import dedent
from blockchain import Blockchain
import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request, render_template,make_response
from flask_cors import *
from flask_wtf import Form
from wtforms import StringField,SubmitField,DecimalField
from wtforms.validators import DataRequired
from blockchain import MyForm, Register_Form
from datetime import datetime
from datetime import timedelta
from threading import Timer
#import sched
from apscheduler.schedulers.background import BackgroundScheduler

from student import Student_Manager
from teacher import Teacher_Manager
from course import Course_Manager
from room_request import Room_request
from room import Room_manager
from flask_pymongo import PyMongo

# Instantiate our Node
app = Flask(__name__)
CORS(app,resources=r'/*')
mongo = PyMongo(app)

active_teachers = []

student_manager = Student_Manager(None)
teacher_manager = Teacher_Manager(None)
course_manager = Course_Manager(None)
room_manager = Room_manager(None)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.before_request
def initial():
    global student_manager , teacher_manager,course_manager
    db = mongo.db
    student_manager = Student_Manager(db)
    teacher_manager = Teacher_Manager(db)
    course_manager = Course_Manager(db)
    room_manager = Room_manager(db)
# Instantiate the Blockchain
blockchain = Blockchain()

### 学生接口

@app.route('/student/login', methods=['POST'])
def get_openid():

    data = request.data
    j_data = yaml.safe_load(data)

    code = j_data['code']
    appid = 'wx8ae9681bcddfcdfe'
    secret = 'b871278e131917f8a793fdfb7c0ad0a9'
    wxurl = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid, secret, code)
    response = requests.get(wxurl)
    res = {}
    openid = json.loads(response.text)['openid'] 
    res['openid'] = openid
    exist = 0
    if student_manager.getstuId(openid):
        exist = 1 #学生已经注册
    res['exist'] = exist 
    return jsonify(res)

#完善信息
@app.route('/student/complete',methods = ['POST'])
def complete_student():

    data = request.data

    j_data = yaml.safe_load(data)

    openid = j_data['openid']
    stuId = j_data['stuId']
    stuName = j_data['stuName']
    avatar = j_data['avatar']

    res = student_manager.addStudent(openid,stuId,stuName,avatar)
    return json.dumps({'response_code':int(res)})


#查看信息(学号和姓名)
@app.route('/student/personalinfo',methods = ['POST'])
def student_personal_info():
    data = request.data

    j_data = yaml.safe_load(data)

    openid = j_data['openid']
    return student_manager.getStudentbyopenid(openid)

#查看签到(返回的是签到记录列表)
@app.route('/student/registerinfo',methods= ['POST'])
def student_register_info():
    data = request.data

    j_data = yaml.safe_load(data)

    openid = j_data['openid']
    
    lis =  student_manager.getRegisterListbyopenid(openid)

    print(lis)
    dic = {"stuName":[],"stuId":[],"courseName":[],"timestamp":[]}
    
    res = []
    if lis:
        for l in lis:
            dic["stuName"] = student_manager.getstuName(l["openid"])
            dic["stuId"] = student_manager.getstuId(l["openid"])
            dic["courseName"] = course_manager.getCourseName(l["courseId"])
            dic["timestamp"] = l["timestamp"]
            res .append(copy.deepcopy(dic))
        return json.dumps([{"response_code":1},res])
    else:
        return json.dumps([{"response_code":0}])

#签到(返回的是response_code)
@app.route('/student/register',methods=['POST'])
def student_register():
    data = request.data

    j_data = yaml.safe_load(data)
    
    openid = j_data['openid']
    courseId = j_data['courseId']
    timestamp = j_data['timestamp']

    res = student_manager.register(openid,courseId,timestamp)

    stuId = student_manager.getstuId(openid)
    # 学生签到，加入对应的课程群, 重复加入没事，去重了
    room_manager.joinRoom(stuId,courseId)

    blockchain.new_transaction(
        sender=openid,
        recipient=courseId,
        amount=1,
    )

    if res == -2:
        return json.dumps({"response_code":-2})
    elif res == -1:
        return json.dumps({"response_code":-1})
    else:
        return json.dumps({"response_code":1})

#获取房间列表
@app.route('/student/course_list',methods=['POST'])
def getCourseListByOpenid():
    data = request.data

    j_data = yaml.safe_load(data)

    openid = j_data['openid']

    return student_manager.getCoursesByOpenid(openid)
#拉取房间所有属性
@app.route('/room/get_room',methods=['POST'])
def get_room():

    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    #return room_manager.getMessage(room_id)
    return room_manager.getRoombyroomid(room_id)
#发送消息
@app.route('/room/send_message',methods = ['POST'])
def room_send_message():

    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    openid = j_data['open_id']
    message = j_data['message']
    stuId = student_manager.getstuId(openid)

    return room_manager.addMessageByStudent(room_id,stuId,message)

#清空消息
@app.route('/room/clear_message',methods = ['POST'])
def room_clear_message():

    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    return room_manager.clearMessage(room_id)

### 教师接口

# 登录
@app.route('/teacher/login',methods=['POST'])
def teacher_login():
    global active_teachers
    data = request.data

    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    password = j_data['password']

    res = teacher_manager.checkPassword(teacherId,password)

    if(res):
        active_teachers.append(teacherId)
        #s = sched.scheduler(time.time, time.sleep)
        #s.enter(600, 0, teacher_logout, (teacherId,))
        #s.run()
        scheduler = BackgroundScheduler()
        scheduler.add_job(teacher_logout, 'date', run_date = timedelta(minutes=1) + datetime.now(), args=[teacherId,])
        scheduler.start()
    
    result_text = {"response_code":int(res)}
    response = make_response(jsonify(result_text))
    #response = json.dumps({"response_code":int(res)})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'    
    #return json.dumps({"response_code":int(res)})
    return response

# 登出
@app.route('/teacher/logout',methods=['POST'])
def teacher_logout(*teacherId):
    global active_teachers

    if(teacherId):
        try:
            active_teachers.remove(teacherId[0])
        except:
            return json.dumps({"response_code":0})
        else:
            return json.dumps({"response_code":1})

    else:
        data = request.data
        j_data = yaml.safe_load(data)
        teacherID = j_data['teacherId']
        try:
            active_teachers.remove(teacherID)
        except:
            return json.dumps({"response_code":0})
        else:
            return json.dumps({"response_code":1})

# 查询教师是否已登录
@app.route('/teacher/ifreg',methods=['POST'])
def if_reg():
    data = request.data
    j_data = yaml.safe_load(data)
    teacherId = j_data['teacherId']
    if teacherId in active_teachers:
        result_text = {"response_code":1}
        response = make_response(jsonify(result_text))
        return response
    else:
        result_text = {"response_code":0}
        response = make_response(jsonify(result_text))
        return response

#查看教师信息
@app.route('/teacher/info',methods=['POST'])
def teacher_info():
    data = request.data

    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    
    res =  teacher_manager.getTeacherbyteacherid(teacherId)

    response = make_response(res)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

    return response

#修改密码
@app.route('/teacher/resetPassword',methods=['POST'])
def resetPassword():
    data = request.data
    j_data = yaml.safe_load(data)
    
    teacherId = j_data['teacherId']
    new_password = j_data['new_password']
    old_password = j_data['old_password']

    res =  teacher_manager.resetPassword(teacherId,new_password,old_password)

    response =make_response(res)        
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

    return response

#查看所教授的所有课程以及对应的courseId
@app.route('/teacher/courseInfo',methods=['POST'])
def courseInfo():
    data = request.data
    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']

    lis = teacher_manager.getteacherCourses(teacherId)

    #print (lis)
    dic = {"courseName":'',"courseId":''}
    res = []
    if lis:
        for iter in lis:
            dic["courseId"] = course_manager.getCourseId(iter)
            dic["courseName"] = iter
            #print (dic)
            res.append(copy.deepcopy(dic))
            #print(res)
        result_text = [{"response_code":1 }, res]
        response = make_response(json.dumps(result_text))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        #return json.dumps([{"response_code":1},res]) 
        return response
    else:
        result_text = {"response_code":0}
        response = make_response(jsonify(result_text))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

        #return json.dumps({"response_code":0})
        return response
    
#添加课程
@app.route('/teacher/addCourse',methods=['POST'])
def addCourse():
    data = request.data
    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    course_name = j_data['course_name']

    res = teacher_manager.addCourse(teacherId,course_name)

    response =make_response(res)        
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

    return response

#删除课程
@app.route('/teacher/delCourse',methods=['POST'])
def delCourse():
    data = request.data
    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    courseId = j_data['courseId']

    res = teacher_manager.deleteCourseById(teacherId,courseId)

    response =make_response(json.dumps({"response_code":int(res)}))        
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

    return response

#查看课程签到记录
@app.route('/teacher/registerList',methods=['POST'])
def teacher_register_info():
    data = request.data
    j_data = yaml.safe_load(data)

    print(j_data)
    courseId = j_data['courseId']
    
    print(courseId)
    lis = teacher_manager.getRegisterListbyCourseId(courseId)
    res = []
    print(lis)
    #dic = {"stuName":[],"stuId":[],"courseName":[],"timestamp":[]}
    dic ={}
    if lis:
        for l in lis:
            dic["stuName"] = student_manager.getstuName(l["openid"])
            dic["stuID"] = student_manager.getstuId(l["openid"])
            dic["courseName"] = course_manager.getCourseName(l["courseId"])
            dic["timestamp"] = l["timestamp"]
            res .append(copy.deepcopy(dic))

        print(res)
        result_text = [{"response_code":1 }, res]
        response = make_response(json.dumps(result_text))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        #return json.dumps([{"response_code":1},res]) 
        return response
    else:
        result_text = {"response_code":0}
        response = make_response(jsonify(result_text))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

        #return json.dumps({"response_code":0})
        return response


#@app.route('/mine', methods=['GET'])
def mine(inc):

    global blockchain
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    '''
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return render_template("mine.html", response_message=response)
    '''
    #print("A block has been mined.")
    t = Timer(inc, mine, (inc,))
    t.start()


@app.route('/transactions', methods=['GET','POST'])
def new_transaction():
    '''
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    '''
    global blockchain
    form = MyForm(csrf_enabled=False)
    if form.validate_on_submit():
        amount = form.data['amount']
        index = blockchain.new_transaction(form.data['sender'], form.data['recipient'], int(amount))
        response = {'message': f'Transaction will be added to Block {index}'}
        return render_template("new_transaction.html",message=response)

    return render_template('new_transaction.html',form=form)


@app.route('/chain', methods=['GET'])
def full_chain():
    global blockchain
    '''
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    
    return render_template("chain.html",chain=blockchain.chain,length=len(blockchain.chain))
    '''
    result_text = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    response = make_response(jsonify(result_text))
    return response
    

@app.route('/pure_chain', methods=['GET'])
def pure_chain():
    global blockchain
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/', methods=['GET'])
def hello():
    return render_template("index.html")


@app.route('/register', methods=['GET','POST'])
def register_nodes():
    '''
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201
    '''
    global blockchain
    form = Register_Form(csrf_enabled=False)
    if form.validate_on_submit():
        node = form.data['node']
        blockchain.register_node(node)
        response = {'message': f'new node {node} has been recorded'}
        return render_template("register.html",message=response)

    return render_template('register.html',form=form)


@app.route('/resolve', methods=['GET'])
def consensus():
    global blockchain
    replaced = blockchain.resolve_conflicts()

    if replaced:
        message='Our chain was replaced'
    else:    
        message='Our chain is authoritative'        

    return render_template("resolve.html",message=message,chain=blockchain.chain)
    #return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    mine(10)

    app.run(host='0.0.0.0', port=port)
