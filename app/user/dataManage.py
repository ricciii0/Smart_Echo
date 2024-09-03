from distutils.file_util import write_file
from fileinput import filename
from sqlite3.dbapi2 import sqlite_version_info
from typing import final
from datetime import datetime
import pymysql.cursors
from flask import after_this_request
from pymysql import connect

import os

'''
在这份文件中，功能主要以函数为组织
函数功能包括
添加文件到资料管理系统

'''
# 定义全局变量
host='localhost'
user='root'
password='0215Wy1330'
db='data_test'

def getconnection():
    #连接函数，进行数据库的连接
    # host即为数据库地址，这里面是本地
    # user是指用户名
    # 还有password 密码
    # 然后是database 即数据库选那个
    # 最后是cursorclass应该是指定查询结果的返回形式，这里指定的是字典光标，应该返回的是字典形式8
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

#之前测试用的main函数
def main():
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            # 执行 SQL 查询
            # *是指所有列，FROM表名，所以语句的意思就是从teacher表选取所有列
            sql = "SELECT * FROM teacher"  # 替换为你实际的表名
            cursor.execute(sql)
            # 获取所有结果
            results = cursor.fetchall()
            for row in results:
                print(row)  # 每一行是一个字典，列名作为键
    finally:
        # 关闭数据库连接
        connection.close()

#存储文件
def storefile(filename,filepath,category="DefaultFolder"):
    connection = getconnection()
    # python中with的用法主要是为了简化资源管理
    try:
        with connection.cursor() as cursor:
            # with语句，file就是open()函数返回的对象
            with open(filepath,'rb') as file:
                file_content = file.read()
                # 书写sql语句
                sql= "INSERT INTO files(filename,filecontent,subject) VALUES (%s,%s,%s)"
                cursor.execute(sql, (filename, file_content, category))
            connection.commit()
    finally:
        #with 语句自动管理对象和游标的关闭，不会自动关闭数据库，所有还需要手动调用close
        connection.close()


#文件下载的功能
def getfile(filename, outputpath):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT filecontent FROM files WHERE filename=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(filename,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            if results:
                with open(outputpath,'wb') as file:
                    file.write(results['filecontent'])
    finally:
        connection.close()


# 通过关键词查询文件
def seekfile(keyword):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql= "SELECT filename FROM files WHERE filename LIKE %s"
            cursor.execute(sql,(f'%{keyword}%',))
            results = cursor.fetchall()
            if results:
                for filename in results:
                    print(filename)
            else:
                print("搜索为空,请检查输入有无错别字等")
    finally:
        connection.close()

#筛选功能模块
def filterfiles(timebegin,timeend,subject):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM files WHERE uploadtime BETWEEN %s AND %s AND subject=%s"
            cursor.execute(sql, (timebegin,timeend,subject))
            afterfiles = cursor.fetchall()
            if afterfiles:
                for file in afterfiles:
                    print(f"fileid={file['id']} filename={file['filename']} ")
            else:
                print("没有结果哦，请重新检查你的筛选")

    finally:
        connection.close()


# 删除功能模块
def deletefile(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql= "DELETE FROM files WHERE id = %s"
            cursor.execute(sql,(id,))
            connection.commit()
    finally:
        connection.close()

#更新文件内容的函数
def updatefile(id,newfilepath):
    newfilename=os.path.basename(newfilepath)
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            with open(newfilepath,'rb') as file:
                file_content = file.read()
                sql= "UPDATE files SET filename=%s,filecontent=%s WHERE id=%s"
                cursor.execute(sql,(newfilename, file_content, id))
            #如果不使用commit()的话无法保存更改记录
            connection.commit()
    finally:
        connection.close()


#批量导入的功能函数
def batchimport(folder):
    filenames = os.listdir(folder)
    filepaths = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        storefile(filename,filepath)
    print(f"批量添加成功")

#清空数据库的函数
def deletedata():
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "TRUNCATE TABLE files"
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()





if __name__ == '__main__':
    main()
    filepath="C:\\Users\\86137\\Desktop\\output1.txt"
    filename=os.path.basename(filepath)
    #storefile(filename,filepath)

    seekfile("图")

    folderpath = "C:\\Users\\86137\\Desktop\\sqltest\\input"
    # batchimport(folderpath)

    # updatefile(1,filepath)

    #deletedata()

    # 获取当前时间
    now = datetime.now()

    # 格式化为 '2024-01-01' 格式
    formatted_date = now.strftime('%Y-%m-%d')
    print(formatted_date)

    filterfiles("2024-09-03 09:50:04","2024-09-03 19:50:04","DefaultFolder")




    # out_path="C:\\Users\\86137\\Desktop\\output1.pptx"
    # getfile(filename,out_path)

