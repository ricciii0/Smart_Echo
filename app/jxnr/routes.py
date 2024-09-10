import os
import io
from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename
from db import db
from models.teaching import TeachingFile as File

# 创建蓝图对象
app_blueprint = Blueprint('app_blueprint', __name__)

from flask_cors import CORS  # 导入CORS库

CORS(app_blueprint, supports_credentials=True)  # 启用CORS，允许跨域请求

# 文件上传目录（未使用，因为文件存储在数据库中）
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx'}

# 判断文件类型是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#搜索文件
from datetime import datetime

@app_blueprint.route('/search_material', methods=['GET'])
def search_material():
    filename = request.args.get('filename')  # 获取文件名查询参数
    date_str = request.args.get('date')  # 获取日期查询参数

    query = File.query

    # 按文件名过滤
    if filename:
        query = query.filter(File.filename.like(f"%{filename}%"))  # 使用模糊匹配来搜索文件名

    # 按上传日期过滤（假设日期格式为 'YYYY-MM-DD'）
    if date_str:
        try:
            # 将字符串转换为日期对象，并过滤该天的文件
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            start_of_day = datetime.combine(date_obj, datetime.min.time())
            end_of_day = datetime.combine(date_obj, datetime.max.time())
            query = query.filter(File.uploadtime >= start_of_day, File.uploadtime <= end_of_day)
        except ValueError:
            return jsonify({"message": "Invalid date format. Use 'YYYY-MM-DD'."}), 400

    files = query.all()  # 获取所有匹配的文件

    if not files:
        return jsonify({"message": "No materials found", "status_code": 404}), 404

    result = []
    for file in files:
        result.append({
            "id": file.id,
            "filename": file.filename,
            "subject": file.subject,
            "uploadTime": file.uploadtime
        })

    return jsonify(result), 200




#下载文件
@app_blueprint.route('/download_material/<int:file_id>', methods=['GET'])
def download_material(file_id):
    file = File.query.get(file_id)

    if not file:
        return jsonify({"message": "Material not found"}), 404

    try:
        # 使用 download_name 替换 attachment_filename
        return send_file(
            io.BytesIO(file.filecontent),  # 将二进制数据转换为流
            download_name=file.filename,  # 设置下载的文件名
            as_attachment=True  # 强制下载
        )
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

#预览文件
@app_blueprint.route('/preview_material/<int:file_id>', methods=['GET'])
def preview_material(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({"message": "Material not found"}), 404

    # 预览文件，不作为附件下载
    return send_file(
        io.BytesIO(file.filecontent),  # 将二进制数据转换为流
        download_name=file.filename,   # 设置文件名
        as_attachment=False            # 设置为 False 以预览
    )


@app_blueprint.route('/delete_material/<int:file_id>', methods=['DELETE'])
def delete_material(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({"message": "Material not found"}), 404

    # 删除文件记录
    db.session.delete(file)
    db.session.commit()

    return jsonify({"message": "Material deleted successfully"}), 200

#上传文件
@app_blueprint.route('/upload_material', methods=['POST'])
def upload_material():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']
    subject = request.form.get('subject')

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = file.filename  # 直接使用原始文件名
        file_data = file.read()  # 读取文件的二进制数据

        new_file = File(filename=filename, subject=subject, filecontent=file_data)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"message": "File type not allowed"}), 400
