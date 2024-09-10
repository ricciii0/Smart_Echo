from flask import Blueprint, jsonify, request, Response

from app.onlineExercise.onlineExercise import create_exercise

oe_bp=Blueprint('oe_bp',__name__,url_prefix='/oe')


@oe_bp.route('/upload/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return '没有选择文件', 400
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    targetclass = request.form.get('targetclass')
    title = request.form.get('title')
    teacherid = request.form.get('teacherid')
    # 这个file是一个特殊的数据结构，好像是从前端那里来的
    file_data = file.read()
    create_exercise(teacherid,targetclass,title,file_data)
    return '文件上传成功'