from flask import Flask, redirect, url_for
from app.auth import auth_bp
from app.user import user_bp
#from config import Config

def create_app():
    app = Flask(__name__)
    #app.config.from_object(Config)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # 设置根路径重定向到登录页面
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
