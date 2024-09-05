好的，以下是一个使用 Flask 框架、SQLAlchemy、LoginManager 和 MySQL 实现的登录、注册和找回密码功能的示例。这个示例使用了 Flask 的 `Blueprint` 来封装这些功能，并设置了相应的路由。

首先，确保你已经安装了 Flask、Flask-SQLAlchemy、Flask-Login 和 MySQL 驱动。

```bash
pip install Flask Flask-SQLAlchemy Flask-Login mysqlclient
```

### 项目结构

```
myapp/
│
├── app.py
├── config.py
├── models.py
├── auth/
│   ├── __init__.py
│   ├── routes.py
│
└── templates/
    ├── login.html
    ├── register.html
    └── forget.html
```

### 配置文件 `config.py`

```python
import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/yourdatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 主应用文件 `app.py`

```python
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from auth.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/')

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
```

### 数据模型 `models.py`

```python
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    account_number = db.Column(db.String(10), unique=True, nullable=False)
```

### Blueprint 路由 `auth/routes.py`

```python
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password, method='sha256')
        account_number = generate_account_number()  # You should implement this function
        new_user = User(username=username, password=hashed_password, email=email, account_number=account_number)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Implement password reset logic here (e.g., send an email)
            return 'Password reset link sent'
        else:
            return 'Email not found'
    return render_template('forget.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
```

### HTML 模板文件

`templates/login.html`

```html
<!doctype html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <a href="{{ url_for('auth.register') }}">Register</a><br>
    <a href="{{ url_for('auth.forget') }}">Forgot Password</a>
</body>
</html>
```

`templates/register.html`

```html
<!doctype html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="email" name="email" placeholder="Email" required><br>
        <button type="submit">Register</button>
    </form>
    <a href="{{ url_for('auth.login') }}">Login</a><br>
    <a href="{{ url_for('auth.forget') }}">Forgot Password</a>
</body>
</html>
```

`templates/forget.html`

```html
<!doctype html>
<html>
<head>
    <title>Forgot Password</title>
</head>
<body>
    <h1>Forgot Password</h1>
    <form method="POST">
        <input type="email" name="email" placeholder="Email" required><br>
        <button type="submit">Send Reset Link</button>
    </form>
    <a href="{{ url_for('auth.login') }}">Login</a><br>
    <a href="{{ url_for('auth.register') }}">Register</a>
</body>
</html>
```

### 生成账户号码的函数

你需要实现一个函数来生成唯一的 10 位账户号码。你可以使用随机生成和唯一性检查的方法。

```python
import random

def generate_account_number():
    while True:
        account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if not User.query.filter_by(account_number=account_number).first():
            return account_number
```

以上是一个基本的实现，你可以根据需求进一步扩展和优化，比如添加表单验证、改进密码重置功能等。