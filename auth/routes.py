from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from requests import session
from sympy import content

from app import db
from auth import auth_bp
from auth.forms import LoginForm, RegisterForm,ForgotForm
from models.user import User
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import smtplib

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_id=form.user_id.data
        pwd=form.password.data
        user=User.query.filter_by(user_id=user_id).first()
        if user and user.check_password(pwd):
            login_user(user)
            flash('登录成功',category='success')
            if user_id.startswith('1'):
                return redirect(url_for('teacher main'))
            elif user_id.startswith('2'):
                return redirect(url_for('student main'))
    return render_template('login.html', title='登录', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        user_type=form.user_type.data
        password=form.password.data
        password_again=form.password_again.data
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        if password!=password_again:
           flash('两次输入密码不相同',category='danger')
        if not user:
            new_user:User=user(user_type=user_type,name=name,password=password,email=email)
            db.session.add(new_user)
            db.session.commit()
    return render_template('register.html',title='注册',form=form)


@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        receiver_email=request.form['email']
        user=User.query.filter_by(email=email).first()
        if user:
            receiver_name=user.name
            vertification_code=str(random.randint(100000,999999))
            email_content = f"【SmartEcho】您的验证码是：{vertification_code}"
            send_email(content=email_content,receiver_name=receiver_name,receiver_email=receiver_email)
            codes_in=request.form['codes']
            if codes_in==vertification_code:
                session['user_reset_pwd']=user
                return redirect(url_for('/auth/forgot/reset'))
    return render_template()

@auth_bp.route('/forgot/reset', methods=['GET', 'POST'])
def reset():
    if request.method == "POST":
        reset_password=request.form['reset_password']
        reset_password_again=request.form['reset_password_again']
        user=session.get('user_reset_pwd')
        if reset_password==reset_password_again:
            user.set_password(reset_password)
        else:
            raise "前后密码不一致！"
    return render_template()

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth/login'))

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
        server.login(sender_email, "tmclbjjmxmmeemvt")  # 你的邮箱账户和密码

        # 发送邮件
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()

        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败，错误信息：{str(e)}")