from flask import Blueprint

# 创建 Student 蓝图
student = Blueprint('student', __name__, url_prefix='/student')


# 导入子蓝图
community_blueprint = Blueprint('community', __name__, url_prefix='/community')

from student.sqjl import routes

student.register_blueprint(community_blueprint)

#注册子蓝图