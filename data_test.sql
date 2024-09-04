-- 清除数据库中同名的表格
DROP DATABASE IF EXISTS `data_test`;
CREATE DATABASE `data_test`;
USE `data_test`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

# 这是资源管理的一张表格
DROP TABLE IF EXISTS files;
CREATE TABLE files(
    id INT(11) NOT NULL AUTO_INCREMENT,
    filename VARCHAR(25) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
    filecontent LONGBLOB NOT NULL,
    subject VARCHAR(25) NULL DEFAULT NULL,
    uploadtime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

# 弄一个在线练习的表格，感觉在线练习的难度会远远大于资料管理
# 所有的表格都是只在服务器端口创建一个，其中不同用户的条目使用用户id进行区分
DROP TABLE IF EXISTS practices;
CREATE TABLE practices(
    id INT(11) NOT NULL AUTO_INCREMENT,
    class VARCHAR(25) NOT NULL

);





INSERT INTO `Teacher`(id, name) VALUES
(1,'449'),
(2,'梁耀欣');