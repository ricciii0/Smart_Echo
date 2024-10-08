from flask import Blueprint, flash, jsonify,session,request
from flask_login import login_user, login_required, logout_user, current_user
from requests import Session
from datetime import timedelta
from mydatabase import db
from wtforms.validators import email
from models.user import User
from models.teacher import Teacher
from models.student import Student
from email.mime.text import MIMEText
from email.utils import formataddr
from flask_cors import CORS  # 导入CORS库
import random
import smtplib



auth=Blueprint('auth', __name__)

CORS(auth, supports_credentials=True)  # 启用CORS，允许跨域请求

# @auth.route('/login/', methods=['POST','GET'])
# def login():
#     if request.method == "POST":
#         data = request.get_json()
#         print(data)
#         if not data:
#             return jsonify({'error':'Invalid data'}), 400
#         user_id = data['user_id']
#         password = data['password']
#         user=User.query.filter_by(user_id=user_id).first()
#         if user and user.check_password(password):
#             login_user(user)
#             user_type=" "
#             if user_id.startswith('1'):
#                 user_type='teacher'
#             if user_id.startswith('2'):
#                 user_type='student'
#             return jsonify({
#                 'message':'login successfully',
#                 'user_type':user_type,
#                 'success':True
#             }),201
#         else:
#             return jsonify({'error':'Invalid user id or password'}), 401
#     else:
#         return jsonify({'error':'Method not allowed'}), 405

@auth.route('/login/', methods=['POST','GET'])
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
            user_type = 'teacher' if user_id.startswith('1') else 'student' if user_id.startswith('2') else None
            return jsonify({
                'message':'login successfully',
                'user_type': user_type,  # 返回用户类型
                'success':True
            }), 201
        else:
            return jsonify({'error':'Invalid user id or password'}), 401
    else:
        return jsonify({'error':'Method not allowed'}), 405

@auth.route('/register/', methods=['POST','GET'])
def register():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        # user_type=data['user_type']
        # user_id=data['user_id']
        user_type = data.get('user_type')
        user_id = data.get('user_id')
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')



        if user_type == 'teacher':
            # name=data['name']
            # password=data['password']
            # subject=data['subject']
            # email=data['email']
            # class1=data['class1']
            # class2=data['class2']
            subject = data.get('subject')
            class1 = data.get('class1')
            class2 = data.get('class2')

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
            # name=data['name']
            # password=data['password']
            # class_id=data['class_id']
            # email=data['email']
            class_id = data.get('class_id')

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


@auth.route('/forgot/', methods=['GET', 'POST'])
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
                session.permanent = True
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

@auth.route('/forgot/verify/', methods=['GET', 'POST'])
def forgot_verify():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        verify_code=session.get('verify_code')
        print(verify_code)
        input_code=data['input_code']
        print(input_code)
        if verify_code==input_code:
            return jsonify({'messages':'Ready to reset password'}),200
        else:
            return jsonify({'error':'Wrong code'}), 401

@auth.route('/forgot/reset/', methods=['GET', 'POST'])
def reset():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error':'Invalid data'}), 400
        password=data['password']
        user_email=session['user_email']
        user=User.query.filter_by(email=user_email).first()
        user.set_password(password)
        print(user.name)
        print(user.password)
        return jsonify({'messages':'Password reset successfully'}),200

@auth.route('/logout/',methods=['POST'])
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

#新增代码：
@auth.route('/resources/', methods=['GET'])
def get_resource_detail():
    # 获取当前登录用户的资源信息
    user = current_user  # 通过 current_user 获取当前登录的用户
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # 假设 User 模型中有一个资源字段
    resource_data = {
        'id': user.id,
        'name': user.name,  # 用户名或者资源名称
        'description': user.email  # 假设使用邮箱模拟资源描述
    }

    return jsonify(resource_data), 200

@auth.route('/user-info/', methods=['GET'])
def get_user_info():
    user = current_user  # 当前登录用户的实例

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_info = {
        'username': user.name,  # 假设User模型中有name字段表示用户名
        'email': user.email,  # 假设User模型中有email字段
        'user_type': user.user_type  # 用户类型
    }

    return jsonify(user_info), 200


@auth.route('/classes/', methods=['GET'])
def get_class_list():
    # 假设班级信息存储在User模型中的class_id字段，返回当前用户的班级信息
    user = current_user  # 获取当前登录用户

    if not user:
        return jsonify({'error': 'User not found'}), 404

    class_info = {
        'id': user.id,
        'class_name': user.class_id  # 假设class_id是班级名称或ID
    }

    return jsonify([class_info]), 200  # 返回当前用户的班级信息

@auth.route('/sidebar-links', methods=['GET'])
def get_sidebar_links():
    role = request.args.get('role')  # 从请求参数中获取用户角色
    if role == 'student':
        links = ['student_link1', 'student_link2']
    elif role == 'teacher':
        links = ['teacher_link1', 'teacher_link2']
    else:
        links = ['default_link']

    return jsonify({'links': links}), 200

