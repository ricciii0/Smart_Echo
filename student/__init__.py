from flask import Blueprint

# 创建 Student 蓝图
student = Blueprint('student', __name__, url_prefix='/student')

# 导入子蓝图


#注册子蓝图