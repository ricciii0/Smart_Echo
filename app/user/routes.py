from flask import render_template
from app.user import user_bp

@user_bp.route('/user_page')
def user_page():
    pass
