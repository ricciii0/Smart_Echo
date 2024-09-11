-- 清除数据库中数据库
# DROP DATABASE IF EXISTS `data_test`;
# CREATE DATABASE `data_test`;

USE `data_test`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS files;
CREATE TABLE files(
    id INT(11) NOT NULL AUTO_INCREMENT,
    teaid INT(11) NOT NULL,
    filename VARCHAR(25) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
    filecontent LONGBLOB NOT NULL,
    subject VARCHAR(25) NULL DEFAULT NULL,
    uploadtime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

# 弄一个在线练习的表格，感觉在线练习的难度会远远大于资料管理
# 所有的表格都是只在服务器端口创建一个，其中不同用户的条目使用用户id进行区分


#用于存储学生提交的答案及成绩 submission表
DROP TABLE IF EXISTS submissions;
CREATE TABLE submissions (
    id INT(11) NOT NULL AUTO_INCREMENT,
    studentid INT(11) NOT NULL,
    targetclass VARCHAR(25) NOT NULL,
    teacherid INT(11) NOT NULL,
    title VARCHAR(25) NOT NULL,
    createtime DATETIME DEFAULT CURRENT_TIMESTAMP,
    exercisecontent LONGBLOB NOT NULL,
    answer LONGBLOB DEFAULT NULL,

    grade VARCHAR(25) DEFAULT NULL,
    feedback VARCHAR(25) DEFAULT NULL,
    #这是学生提交的时间
    submittime DATETIME DEFAULT NULL,
    #这是批改的时间
    correcttime DATETIME DEFAULT NULL,
    PRIMARY KEY (id)
);




