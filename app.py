from flask import Flask, redirect, url_for, jsonify
from mydatabase import db
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

from auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
@app.route('/')
def index():
    return jsonify({'message':'fuck u seu'})


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

