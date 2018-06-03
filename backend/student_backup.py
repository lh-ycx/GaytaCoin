# -*- coding: UTF-8 -*-


import numpy as np
import pandas as pd
from flask import request

stu_data = pd.DataFrame({'openid':[],'name':[],'studentID':[]})
stu_data.to_csv("student.csv", index=False)
stu_data = pd.read_csv("student.csv")

def insert_stu(openid, name, student_id):
    global stu_data
    if student_id in list(stu_data['studentID']):
        print("Your student ID has been registered. Please try again.")
        return
    stu_data = pd.concat([stu_data, pd.DataFrame({'openid':[openid],'name':[name],'studentID':[student_id]})])
    print("Insert successfully.")
    return

insert_stu('aaaaaa','韩佳良',1234567890)
insert_stu('bbbbbb', '杨程旭', 9876543210)
insert_stu('cccccc', '陈正胤', 9876543210)

print(stu_data)
stu_data.to_csv("student.csv", index = False)




def select_stu_name(openid):
    global stu_data
    return stu_data[stu_data['openid']==openid]['name'].values[0]
def select_stu_id(openid):
    global stu_data
    return stu_data[stu_data['openid']==openid]['studentID'].values[0]
print(select_stu_name('aaaaaa'))
print(select_stu_id('aaaaaa'))



