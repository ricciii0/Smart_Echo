import io

from flask import Blueprint, jsonify, request, Response, send_file

rm_bp=Blueprint('rm_bp',__name__,url_prefix='/rm')
from teacher.resourceManage.resourceManage import getsqlResource, storefile, deletefile, getfile, getfilename
from flask_cors import CORS  # 导入CORS库
CORS(rm_bp, supports_credentials=True)  # 启用CORS，允许跨域请求

@rm_bp.route('/print/')
def homeprint():
    aimid = request.args.get('teaid')
    sqlresult = getsqlResource(aimid)

    result = [{
        "id":sqlresult[i]["id"],
        "name":sqlresult[i]["filename"],
        "subject":sqlresult[i]["subject"],
        "uploadTime":sqlresult[i]["uploadtime"],
    } for i in range(len(sqlresult))]
    return jsonify(result)

@rm_bp.route('/printdb/')
def printdb():
    aimid = request.args.get('teaid')
    sqlresult = getsqlResource(aimid)

    result = [{
        "id":sqlresult[i]["id"],
        "name":sqlresult[i]["filename"],
    } for i in range(len(sqlresult))]
    return jsonify(result)

@rm_bp.route('/upload/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return '没有选择文件', 400
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    subject = request.form.get('subject')
    teaid = request.form.get('teaid')
    # 这个file是一个特殊的数据结构，好像是从前端那里来的
    file_data = file.read()
    file_name = file.filename
    storefile(file_name, file_data,subject,teaid)
    return '文件上传成功'

@rm_bp.route('/detele/', methods=['POST'])
def detelefiles():
    data = request.json
    values = data.get('values', [])
    try:
        for id in values:
            deletefile(id)
        return "删除成功"
    except Exception as e:
        #处理其他未预见的异常
        return f"发生错误 - {e}"

@rm_bp.route('/download/', methods=['POST'])
def download():
    # request.get_json()和request.json一样，只是前者更加灵活，后者更加方便
    data = request.get_json()
    resource = data.get('resource')
    aimid = resource['id']
    file_content = getfile(aimid)
    if file_content:
        return Response(
            file_content,
            mimetype='application/octet-stream',
            headers={"Content-Disposition": "attachment;filename=downloaded_file.ext"}
        )
    else:
        return "eaewaeResource not found", 404

@rm_bp.route('/preview_material/<int:file_id>', methods=['GET'])
def preview_material(file_id):
    file_content = getfile(file_id)
    file_name=getfilename(file_id)
    if not file_content:
        return jsonify({"message": "Material not found"}), 404
    return send_file(
        io.BytesIO(file_content),
        download_name=file_name,
        as_attachment=False
    )

