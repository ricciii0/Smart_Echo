# from flask import Flask, redirect, url_for, jsonify
# from flask_cors import CORS
# from mydatabase import db
# from flask_login import LoginManager
# from models.user import User
# app = Flask(__name__)
# CORS(app,supports_credentials=True)
# app.config.from_object('config.Config')
#
# from auth.routes import auth
# app.register_blueprint(auth, url_prefix='/auth')
#
# login_manager = LoginManager(app)
# login_manager.login_view = 'auth.login'
#
# @login_manager.user_loader
# def user_loader(user_id: str):
#     user = User.query.get(user_id)
#     return user
#
# @app.route('/',methods=["GET","POST"])
# def index():
#     return jsonify({'message':'fuck u seu'})
#
#
# if __name__ == '__main__':
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
#
from flask import Flask, jsonify
from flask_cors import CORS
from mydatabase import db
from flask_login import LoginManager
from models.user import User
from auth.routes import auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # 设置一个安全的密钥
app.config.from_object('config.Config')  # 确保您的配置文件正确
CORS(app, supports_credentials=True)

# 初始化数据库
db.init_app(app)

# 设置登录管理
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def user_loader(user_id: str):
    return User.query.get(user_id)

@app.route('/', methods=["GET", "POST"])
def index():
    return jsonify({'message': 'Welcome to the application'})

# 注册蓝图
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保在应用上下文中创建所有表
    app.run(debug=True)