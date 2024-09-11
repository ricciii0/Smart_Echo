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
def create_exercise(teacherid,studentid,title,targetclass,exerciseontent,exercisename):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO submissions(teacherid,studentid,title,targetclass,exercisecontent,exercisename) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(teacherid,studentid,title,targetclass,exerciseontent,exercisename))
            connection.commit()
    finally:
        connection.close()

# 得到还没有做的练习
def getexercise(stuid):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM submissions WHERE studentid=%s AND answer IS NULL"
            cursor.execute(sql, (stuid,))
            result = cursor.fetchall()
    finally:
        connection.close()
        return result

# 得到已经做到的练习
def getsubmission(stuid):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM submissions WHERE studentid=%s AND answer IS NOT NULL"
            cursor.execute(sql, (stuid,))
            result = cursor.fetchall()
    finally:
        connection.close()
        return result

def teagetsubmission(teaid):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM submissions WHERE teacherid=%s AND answer IS NOT NULL"
            cursor.execute(sql, (teaid,))
            result = cursor.fetchall()
    finally:
        connection.close()
        return result

#文件下载的功能
def gettheFile(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT exercisecontent FROM submissions WHERE id=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(id,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            return results['exercisecontent']
    finally:
        connection.close()

def gettheFile_name(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT exercisename FROM submissions WHERE id=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(id,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            return results['exercisename']
    finally:
        connection.close()


#文件下载的功能
def getstusubmission(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT answer FROM submissions WHERE id=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(id,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            return results['answer']
    finally:
        connection.close()

def getstusubmissionname(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT answername FROM submissions WHERE id=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(id,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            return results['answername']
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
def stu_submit(exerciseid,answer,answername):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            update_query = """
            UPDATE submissions
            SET answer = %s,submittime=%s,answername=%s
            WHERE id = %s
            """
            now = datetime.now()
            formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(update_query,(answer,formatted_datetime,answername,exerciseid))
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
            sql = "UPDATE submissions SET grade=%s,feedback=%s,correcttime=%s WHERE id =%s"
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

