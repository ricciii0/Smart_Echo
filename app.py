from flask import Flask, redirect, url_for, jsonify
from db import db  # 修改为从 db.py 导入
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

# 导入身份验证相关的蓝图
from auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

# 导入教学内容相关的蓝图
from app.jxnr.routes import app_blueprint as jxnr_blueprint
app.register_blueprint(jxnr_blueprint, url_prefix='/jxnr')

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the main app'})

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


