# <center><font face="宋体" font color=orange>SmartEcho智能教学助手</font>
这是一个seu小组的暑期学校实训项目罢了~

文件结构：
/frontend       前端
/models         存储sqlalchemy的类
/auth           登录注册的功能
/student        学生的所有功能 
/teacher        教师的所有功能
mydatabse.py    创建sqlalchemy实例
config.py       配置信息
requirements.txt 依赖
app.py          项目入口


url structure:
auth/login                      //初始页面
----/register             //注册 成功后返回到登录
----/forgot
----/forgot/verify
----/forgot/reset
//以上已经实现
//以下还需努力
/student                    //学生主页面

--------/quiz               //查看习题
-------------/****/detail   //****习题号对应习题内容
-------------/****/submit   //****习题号对应习题提交

--------/course             //查看课程资料
---------------/

--------/question           //提问

--------/discussion         //讨论

--------/information        //个人学情

/teacher                    //教师主页面
--------/quiz               //布置习题
--------/course             //布置讲义
--------/question           //人工答疑
--------/discussion         //讨论
--------/information        //学生学情


项目运行前请先cd .\frontend\
然后在命令行输入npm run dev编译
