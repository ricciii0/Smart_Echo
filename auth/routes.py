from flask import Blueprint, flash, jsonify,session,request
from flask_login import login_user, login_required, logout_user, current_user
from mydatabase import db
from wtforms.validators import email
from models.user import User
from models.teacher import Teacher
from models.student import Student
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import smtplib

auth=Blueprint('auth', __name__)

@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        user_id = data['user_id']
        password = data['password']
        user=User.query.filter_by(user_id=user_id).first()
        if user and user.check_password(password):
            login_user(user)
            user_type=" "
            if user_id.startswith('1'):
                user_type='teacher'
            if user_id.startswith('2'):
                user_type='student'
            return jsonify({
                'message':'login successfully',
                'user_type':user_type
            }),201
        else:
            return jsonify({'error':'Invalid user id or password'}), 401
    else:
        return jsonify({'error':'Method not allowed'}), 405

@auth.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        user_type=data['user_type']
        user_id=data['user_id']
        if user_type == 'teacher':
            name=data['name']
            password=data['password']
            subject=data['subject']
            email=data['email']
            class1=data['class1']
            class2=data['class2']
            user=User.query.filter_by(user_id=user_id).first()
            if user:
                return jsonify({'error':'Teacher already registered'}), 400
            new_teacher_user=User(
                user_id=user_id,
                user_type='teacher',
                name=name,
                password=password,
                email=email
            )
            new_teacher = Teacher(
                user_id=user_id,
                subject=subject,
                class1=class1,
                class2=class2
            )
            try:
                db.session.add(new_teacher_user)
                db.session.commit()
                db.session.add(new_teacher)
                db.session.commit()
                return jsonify({'message': 'Teacher registered successfully'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Registration failed', 'details': str(e)}), 500
        if user_type == 'student':
            name=data['name']
            password=data['password']
            class_id=data['class_id']
            email=data['email']
            user=User.query.filter_by(user_id=user_id).first()
            if user:
                return jsonify({'error':'Student already registered'}), 400
            new_student_user=User(
                user_id=user_id,
                user_type='student',
                name=name,
                password=password,
                email=email
            )
            new_student = Student(
                user_id=user_id,
                class_id=class_id
            )
            try:
                db.session.add(new_student_user)
                db.session.commit()
                db.session.add(new_student)
                db.session.commit()
                return jsonify({'message': 'Student registered successfully'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Registration failed', 'details': str(e)}), 500


@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        receiver_email=data['receiver_email']
        if email(receiver_email):
            user = User.query.filter_by(email=receiver_email).first()
            if user:
                verify_code=str(random.randint(100000,999999))
                session['verify_code']=verify_code
                session['user_email']=receiver_email
                receiver_name=user.name
                email_content = f"【SmartEcho】您的验证码是：{verify_code}"
                send_email(content=email_content, receiver_name=receiver_name, receiver_email=receiver_email)
                return jsonify({'messages':'Email successfully send'}),200
            else:
                return jsonify({'error':'No such user'}),401
        else:
            return jsonify({'error':'Invalid email address'}), 401

@auth.route('/forgot/verify', methods=['GET', 'POST'])
def forgot_verify():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        verify_code=data['verify_code']
        input_code=data['input_code']
        if verify_code==input_code:
            return jsonify({'messages':'Ready to reset password'}),200
        else:
            return jsonify({'error':'Wrong code'}), 401

@auth.route('/forgot/reset', methods=['GET', 'POST'])
def reset():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        password=data['password']
        user_email=session['user_email']
        user=User.query.filter_by(email=user_email).first()
        user.set_password(password)
        return jsonify({'messages':'Password reset successfully'}),200

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message':'Logout successfully'}), 200


def send_email(receiver_name,receiver_email,content,sender_name="Smart Echo", sender_email="lnarsil131@outlook.com",subject="找回密码" ):
    try:
        # 设置邮件内容
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([sender_name, sender_email])
        msg['To'] = formataddr([receiver_name, receiver_email])
        msg['Subject'] = subject

        # 使用SMTP服务发送邮件
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login(sender_email, "tmclbjjmxmmeemvt")  # 邮箱账户和密码

        # 发送邮件
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()

        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败，错误信息：{str(e)}")