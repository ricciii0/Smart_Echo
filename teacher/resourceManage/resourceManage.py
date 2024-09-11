import os
from datetime import datetime

import pymysql.cursors

'''
在这份文件中，功能主要以函数为组织
函数功能包括
1、添加文件到资料管理系统（支持批量的添加）
2、删除指定的文件
3、根据时间或者科目进行筛洗
4、支持搜索文件名称
5、支持下载文件
6、支持先筛选后搜索文件名称，搜索范围会缩小到筛选后
7、支持更改文件（但好像没啥用）
'''

def getconnection():
    #连接函数，进行数据库的连接
    # host即为数据库地址，这里面是本地
    # user是指用户名
    # 还有password 密码
    # 然后是database 即数据库选那个
    # 最后是cursorclass应该是指定查询结果的返回形式，这里指定的是字典光标，应该返回的是字典形式8
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='ysy200422',
                                 db='teaching_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



#存储文件
def storefile(filename,file_content,category,teaid):
    connection = getconnection()
    # python中with的用法主要是为了简化资源管理
    try:
        with connection.cursor() as cursor:
            # with语句，file就是open()函数返回的对象
            sql= "INSERT INTO files(filename,filecontent,subject,teaid) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (filename, file_content, category,teaid))
            connection.commit()
    finally:
        #with 语句自动管理对象和游标的关闭，不会自动关闭数据库，所有还需要手动调用close
        connection.close()


#文件下载的功能
def getfile(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT filecontent FROM files WHERE id=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(id,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            return results['filecontent']
    finally:
        connection.close()

def getfilename(id):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT filename FROM files WHERE id=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(id,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            return results['filename']
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
                    print(filename['filename'])
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

#尝试把筛选功能和搜索功能进行合并处理，试一下
def seekfilterfiles(timebegin,timeend,subject='',keyword =''):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM files WHERE uploadtime BETWEEN %s AND %s AND subject LIKE %s AND filename LIKE %s"
            cursor.execute(sql, (timebegin,timeend,f'%{subject}%',f'%{keyword}%'))
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


#更新文件内容的函数,好像不是那么的需要
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

def getsqlResource(aimid):
    connection = getconnection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM files WHERE teaid=%s"
            cursor.execute(sql,(aimid,))
            results = cursor.fetchall()
    finally:
        connection.close()
        return results


if __name__ == '__main__':
    filepath="C:\\Users\\86137\\Desktop\\output1.txt"
    filename=os.path.basename(filepath)
    #storefile(filename,filepath)

    #seekfile("")

    folderpath = "C:\\Users\\86137\\Desktop\\sqltest\\input"
    #batchimport(folderpath)

    # updatefile(1,filepath)

    #deletedata()
    getsqlResource()

    # 获取当前时间
    # now = datetime.now()
    #
    # # 格式化为 '2024-01-01' 格式
    # formatted_date = now.strftime('%Y-%m-%d')
    # print(formatted_date)

    #seekfilterfiles("2024-09-03 09:50:04","2024-09-04 19:50:04")




    # out_path="C:\\Users\\86137\\Desktop\\output1.pptx"
    # getfile(filename,out_path)


