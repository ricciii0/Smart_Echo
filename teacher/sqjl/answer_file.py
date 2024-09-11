import io
import random
import string

from flask import jsonify, request, send_file
from werkzeug.utils import secure_filename
from models.answerFile import AnswerFile
from mydatabase import db
from datetime import datetime

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'zip', 'cpp', 'py', 'c'}


def allowed_file(file_name):
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def download_answer_file():
    file_id = request.args.get('file_id')
    file = AnswerFile.query.get(file_id)

    if not file:
        return jsonify({"message": "找不到文件"}), 404

    try:
        return send_file(
            io.BytesIO(file.file_content),
            download_name=file.file_name,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"error": f": {str(e)}"}), 500


def delete_answer_file():
    file_id = request.get_json().get('file_id')
    file = AnswerFile.query.get(file_id)
    if not file:
        return jsonify({"message": "找不到材料"}), 404

    db.session.delete(file)
    db.session.commit()

    return jsonify({"message": "文件删除成功"}), 200


def upload_answer_file():
    if 'file' not in request.files:
        return jsonify({"message": "缺少文件数据"}), 400

    file = request.files['file']
    user_id = request.form.get('user_id')
    question_id = request.form.get('question_id')
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    count = 0
    files = AnswerFile.query.all()
    if files:
        count = len(files)
    random_chars = ''.join(random.choice(string.ascii_letters) for _ in range(4))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_data = file.read()
        new_file = AnswerFile(file_name=filename, user_id=user_id, question_id=question_id,
                              file_content=file_data, file_id=user_id+'_'+random_chars+'_'+str(count+1))
        db.session.add(new_file)
        db.session.commit()

        return jsonify({'message': '文件上传成功'}), 200
    return jsonify({'error': '文件类型错误'}), 400