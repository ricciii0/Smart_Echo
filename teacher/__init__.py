from flask import Blueprint

# 创建父蓝图 teacher
teacher = Blueprint('teacher', __name__, url_prefix='/teacher')

# 创建子蓝图 teaching_blueprint
teaching_blueprint = Blueprint('teaching', __name__, url_prefix='/teaching')

# 导入子蓝图的路由
from teacher.jxnr import routes  # 确保 routes.py 中的路由绑定到 teaching_blueprint

# 将子蓝图注册到父蓝图
teacher.register_blueprint(teaching_blueprint)


community_blueprint = Blueprint('community', __name__, url_prefix='/community')

from teacher.sqjl import routes

teacher.register_blueprint(community_blueprint)


