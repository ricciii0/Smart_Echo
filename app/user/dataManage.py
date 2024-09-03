from distutils.file_util import write_file
from fileinput import filename

import pymysql.cursors
from pymysql import connect

import os

# 定义全局变量
host='localhost'
user='root'
password='0215Wy1330'
db='data_test'

def main():
    connection = pymysql.connect(host=host,user=user,
                                 password=password,db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
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

def storefile(filename,filepath):
    # host即为数据库地址，这里面是本地
    # user是指用户名
    # 还有password 密码
    # 然后是database 即数据库选那个
    # 最后是cursorclass应该是指定查询结果的返回形式，这里指定的是字典光标，应该返回的是字典形式8
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
    # python中with的用法主要是为了简化资源管理
    try:
        with connection.cursor() as cursor:
            # with语句，file就是open()函数返回的对象
            with open(filepath,'rb') as file:
                file_content = file.read()
                # 书写sql语句
                sql= "INSERT INTO files(filename,filecontent) VALUES (%s,%s)"
                cursor.execute(sql, (filename, file_content))
            connection.commit()
    finally:
        #with 语句自动管理对象和游标的关闭，不会自动关闭数据库，所有还需要手动调用close
        connection.close()


#文件下载的作用
def getfile(filename, output_path):
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT filecontent FROM files WHERE filename=%s"
            # (filename)会被当成单个元素的参数(filename,)是只含有一个元素的元组
            cursor.execute(sql,(filename,))
            # fetchall是提取所有数据，fetchone是提取一行数据
            results = cursor.fetchone()
            if results:
                with open(output_path,'wb') as file:
                    file.write(results['filecontent'])
    finally:
        connection.close()


# 通过关键词查询文件
def seekfile(keyword):
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
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



# 删除功能模块
def deletefile(id):
    connection = pymysql.connect(host=host, user=user,
                                 password=password, db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql= "DELETE FROM files WHERE id = %s"
            cursor.execute(sql,(id,))
            connection.commit()
    finally:
        connection.close()



#批量导入的功能函数
def batchimport(folder):
    filenames = os.listdir(folder)
    filepaths = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    for filpath in filepaths:
        filename = os.path.basename(filpath)
        storefile(filename,filepath)
    print(f"批量添加成功")






if __name__ == '__main__':
    main()
    filepath="C:\\Users\\86137\\Desktop\\绘图2.pdf"
    filename=os.path.basename(filepath)
    #storefile(filename,filepath)

    seekfile("图")

    folderpath = "C:\\Users\\86137\\Desktop\\sqltest\\input"
    #batchimport(folderpath)




    # out_path="C:\\Users\\86137\\Desktop\\output1.pptx"
    # getfile(filename,out_path)


