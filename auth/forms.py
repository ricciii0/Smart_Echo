from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models.user import User,UserType

class LoginForm(FlaskForm):
    user_id = StringField('User_id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    user_type=SelectField('User_type',choices=[(user_type.value, user_type.name.capitalize()) for user_type in UserType],validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    password_again=PasswordField('Password_again', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Register')

class ForgotForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired()])

    submit = SubmitField('Forgot Password')
