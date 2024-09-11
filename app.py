from flask import Flask, jsonify
from flask_cors import CORS
from mydatabase import db
from flask_login import LoginManager
from models.user import User
from auth.routes import auth
from teacher.onlineExercise import oe_bp
from teacher.resourceManage import rm_bp

app = Flask(__name__)

app.config.from_object('config.Config')  # 确保您的配置文件正确
CORS(app, supports_credentials=True)


# 注册蓝图
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(rm_bp)
app.register_blueprint(oe_bp)

# 导入并注册 teacher 蓝图（含有子蓝图）
from teacher import teacher  # 导入 teacher 蓝图
app.register_blueprint(teacher, url_prefix='/teacher')  # 注册 teacher 蓝图

from student import student
app.register_blueprint(student, url_prefix='/student')

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



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保在应用上下文中创建所有表
    app.run(debug=True)