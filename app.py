from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS
from mydatabase import db
from flask_login import LoginManager
from models.user import User

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object('config.Config')

# 导入并注册 auth 蓝图
from auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

# 导入并注册 teacher 蓝图（含有子蓝图）
from teacher import teacher  # 导入 teacher 蓝图
app.register_blueprint(teacher, url_prefix='/teacher')  # 注册 teacher 蓝图

# 设置 LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def user_loader(user_id: str):
    user = User.query.get(user_id)
    return user

# 定义主页路由
@app.route('/')
def index():
    return jsonify({'message':'Welcome to the main app'})

# 应用程序入口
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    print(app.url_map)

# from flask import Flask, jsonify
# from db import db  # 修改为从 db.py 导入
# from flask_login import LoginManager
#
# app = Flask(__name__)
# app.config.from_object('config.Config')
#
# # 导入身份验证相关的蓝图
# from auth.routes import auth
# app.register_blueprint(auth, url_prefix='/auth')
#
# # 导入教学内容相关的蓝图
# from teacher.jxnr import app_blueprint as jxnr_blueprint
# app.register_blueprint(jxnr_blueprint, url_prefix='/jxnr')
#
# login_manager = LoginManager(app)
# login_manager.login_view = 'auth.login'
#
# @app.route('/')
# def index():
#     return jsonify({'message': 'Welcome to the main app'})
#
# if __name__ == '__main__':
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

