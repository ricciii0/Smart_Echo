from mydatabase import db
from flask_login import UserMixin
import datetime
import bcrypt
from enum import Enum


class UserType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"


class User(UserMixin, db.Model):
    user_id = db.Column(db.String(9), primary_key=True)#9位，1开头表示教师，2开头表示学生
    user_type=db.Column(db.Enum(UserType),nullable=False)#教师或学生
    name = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)#bcrypt的密文长度为60字节
    email=db.Column(db.String(60), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self,user_id,user_type, name, password,email):
        self.user_id = user_id
        self.user_type = user_type
        self.name = name
        self.set_password(password)
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return self.user_id


    def set_password(self, password):
        salt=bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password=hashed_password.decode('utf-8')
        db.session.commit()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))