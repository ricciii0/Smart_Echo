from flask import Flask, redirect, url_for, jsonify
from flask_cors import CORS
from mydatabase import db
from flask_login import LoginManager
from models.user import User
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config.from_object('config.Config')

from auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def user_loader(user_id: str):
    user = User.query.get(user_id)
    return user

@app.route('/')
def index():
    return jsonify({'message':'fuck u seu'})


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

