from distutils.file_util import write_file
from fileinput import filename
from sqlite3.dbapi2 import sqlite_version_info
from typing import final
from datetime import datetime
import pymysql.cursors
from flask import after_this_request
from pymysql import connect

'''
在此书写作业管理系统
可以实现的功能包括：
教师端：
1、选择对应的班级进行练习的发布
2、学生接收练习的情况
3、学生进行练习的提交
4、老师给与反馈
5、自动生成历史记录
'''



#这边假设我从cookie中读出了教师的id和同学的id
teacher_id=2
student_id=3

def getconnection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='0215Wy1330',
                                 db='data_test',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# 教师进行练习的创建并发布
def create_exercise(userid,targetclass,title,content):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO exercises(teacherid,targetclass,title,content) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql,(userid,targetclass,title,content))
            connection.commit()
    finally:
        connection.close()

#老师从资料库中上传
def createfromdatabase(userid,targetclass,title,ddl,databaseid):
    # 连接到知识库中
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='0215Wy1330',
                                 db='data_test',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT filecontent FROM files WHERE id=%s"
            cursor.execute(sql,(databaseid,))
            result = cursor.fetchone()
            content=result['filecontent']
            create_exercise(userid,targetclass,title,ddl,content)
    finally:
        connection.close()

# 学生端进行练习的提交
def stu_submit(userid,exerciseid,answer):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            # 去获得teacherid
            sql = "SELECT * FROM exercises WHERE id=%s"
            cursor.execute(sql,(exerciseid,))
            result = cursor.fetchone()
            tea_id = result['teacherid']
            exercise_content=result['content']
            # 写入提交
            sql = "INSERT INTO submissions(studentid,exerciseid,answer,teacherid,execrisecontent) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, (userid,exerciseid,answer,tea_id,exercise_content))
            connection.commit()
    finally:
        connection.close()

# 教师端批改练习
def correct_exercise(grade,feedback,subid):
    connection = getconnection()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE submissions SET grade=%s,feedback=%s,correcttime=%s WHERE id=%s"
            cursor.execute(sql, (grade,feedback,formatted_date,subid))
            connection.commit()
    finally:
        connection.close()

#  获取历史记录，返回？
def stuhistory(studentid):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM exercises WHERE studentid=%s"
            cursor.execute(sql, (studentid,))
            results = cursor.fetchall()
            print(results)
    finally:
        connection.close()

def teahistory(teacherid):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM exercises WHERE studentid=%s"
            cursor.execute(sql, (teacherid,))
            results = cursor.fetchall()
            print(results)
    finally:
        connection.close()

if __name__=='__main__':
    print(111)
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(now)
    print(formatted_date)
    print(formatted_date)

    # filepath = "C:\\Users\\86137\\Desktop\\爬泰山！.md"
    # with open(filepath,'rb') as f:
    #     content = f.read()
    #     create_exercise(teacher_id,2,"数学小测", formatted_date , content)
    #     stu_submit(student_id,1,content)
    # correct_exercise('0分','做的很差','1')

    createfromdatabase(teacher_id,"090221","数学小测",formatted_date,5)

