from flask import render_template, url_for, request, redirect, flash, Blueprint
from app.auth import auth_bp
# from app.auth.forms import LoginForm, RegistrationForm

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    #TODO
    pass

@auth_bp.route('/register',methods=['GET','POST'])
def register():
    #TODO
    pass
