from flask import Blueprint

user_bp=Blueprint('user_bp',__name__,url_prefix='/user')

from app.user import routes