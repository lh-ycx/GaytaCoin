# -*- coding: UTF-8 -*-

import hashlib
import json,yaml
import decimal
import requests
from textwrap import dedent
from blockchain import Blockchain
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request, render_template
from flask_wtf import Form
from wtforms import StringField,SubmitField,DecimalField
from wtforms.validators import DataRequired
from blockchain import MyForm, Register_Form

from student import Student_Manager
from teacher import Teacher_Manager
from course import Course_Manager
from flask_pymongo import PyMongo

# Instantiate our Node
app = Flask(__name__)
mongo = PyMongo(app)

student_manager = Student_Manager(None)
teacher_manager = Teacher_Manager(None)
course_manager = Course_Manager(None)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.before_request
def initial():
    global student_manager , teacher_manager
    db = mongo.db
    student_manager = Student_Manager(db)
    teacher_manager = Teacher_Manager(db)
    course_manager = Course_Manager(db)
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

    res = student_manager.addStudent(openid,stuId,stuName)
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

    dic = {"stuName":[],"stuId":[],"courseName":[],"timestamp":[]}
    
    if lis:
        for l in lis:
            dic["stuName"] = student_manager.getstuName(l["openid"])
            dic["stuId"] = student_manager.getstuId(l["openid"])
            dic["courseName"] = course_manager.getCourseName(l["courseId"])
            dic["timestamp"] = l["timestamp"]
            res .append(dic)
        return json.dumps([{"response_code":1},res])
    else:
        return json.dumps({"response_code":0})

#签到(返回的是response_code)
@app.route('/student/register',methods=['POST'])
def student_register():
    data = request.data

    j_data = yaml.safe_load(data)
    
    openid = j_data['openid']
    courseId = j_data['courseId']
    timestamp = j_data['timestamp']

    return student_manager.register(openid,courseId,timestamp)


### 老司机接口

# 登录
@app.route('/teacher/login',methods=['POST'])
def teacher_login():
    data = request.data

    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    password = j_data['password']

    res = teacher_manager.checkPassword(teacherId,password)
    response = json.dumps({"response_code":int(res)})
    response.addHeader("Access-Control-Allow-Origin", "*")
    #return json.dumps({"response_code":int(res)})
    return response

#查看教师信息
@app.route('/teacher/info',methods=['POST'])
def teacher_info():
    data = request.data

    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    
    return teacher_manager.getTeacherbyteacherid(teacherId)

#修改密码
@app.route('/teacher/resetPassword',methods=['POST'])
def resetPassword():
    data = request.data
    j_data = yaml.safe_load(data)
    
    teacherId = j_data['teacherId']
    new_password = j_data['new_password']
    old_password = j_data['old_password']

    return teacher_manager.resetPassword(teacherId,new_password,old_password)


#查看所教授的所有课程以及对应的courseId
@app.route('/teacher/courseInfo',methods=['POST'])
def courseInfo():
    data = request.data
    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']

    lis = teacher_manager.getteacherCourses(teacherId)

    dic = {"courseName":[],"courseId":[]}
    res = []
    if lis:
        for iter in lis:
            dic["courseId"] = course_manager.getCourseId(iter)
            dic["courseName"] = iter
            res.append(dic)
        response = json.dumps([{"response_code":1},res])
        response.addHeader("Access-Control-Allow-Origin", "*")
        #return json.dumps([{"response_code":1},res]) 
        return response
    else:
        response = json.dumps({"response_code":0})
        response.addHeader("Access-Control-Allow-Origin", "*")
        #return json.dumps({"response_code":0})
        return response
#添加课程
@app.route('/teacher/addCourse',methods=['POST'])
def addCourse():
    data = request.data
    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    course_name = j_data['course_name']

    return teacher_manager.addCourse(teacherId,course_name)

#删除课程
@app.route('/teacher/delCourse',methods=['POST'])
def delCourse():
    data = request.data
    j_data = yaml.safe_load(data)

    teacherId = j_data['teacherId']
    courseId = j_data['courseId']

    res = teacher_manager.deleteCourseById(teacherId,courseId)

    return json.dumps({"response_code":int(res)})

#查看课程签到记录
@app.route('/teacher/registerList',methods=['POST'])
def teacher_register_info():
    data = request.data
    j_data = yaml.safe_load(data)

    courseId = j_data['courseId']

    lis = teacher_manager.getRegisterListbyCourseId(courseId)
    res = []
    dic = {"stuName":[],"stuId":[],"courseName":[],"timestamp":[]}
    if lis:
        for l in lis:
            dic["stuName"] = student_manager.getstuName(l["openid"])
            dic["stuID"] = student_manager.getstuId(l["openid"])
            dic["courseName"] = course_manager.getCourseName(l["courseId"])
            dic["timestamp"] = l["timestamp"]
            res .append(dic)
        return json.dumps([{"response_code":1},res])
    else:
        return json.dumps({"response_code":0})


@app.route('/mine', methods=['GET'])
def mine():
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

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return render_template("mine.html", response_message=response)


@app.route('/transactions', methods=['GET','POST'])
def new_transaction():
    '''
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    '''
    form = MyForm(csrf_enabled=False)
    if form.validate_on_submit():
        amount = form.data['amount']
        index = blockchain.new_transaction(form.data['sender'], form.data['recipient'], int(amount))
        response = {'message': f'Transaction will be added to Block {index}'}
        return render_template("new_transaction.html",message=response)

    return render_template('new_transaction.html',form=form)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    
    return render_template("chain.html",chain=blockchain.chain,length=len(blockchain.chain))
    

@app.route('/pure_chain', methods=['GET'])
def pure_chain():
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
    form = Register_Form(csrf_enabled=False)
    if form.validate_on_submit():
        node = form.data['node']
        blockchain.register_node(node)
        response = {'message': f'new node {node} has been recorded'}
        return render_template("register.html",message=response)

    return render_template('register.html',form=form)


@app.route('/resolve', methods=['GET'])
def consensus():
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

    app.run(host='0.0.0.0', port=port)
