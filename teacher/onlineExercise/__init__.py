from fileinput import filename
import io

from flask import Blueprint, jsonify, request, Response, send_file

from teacher.onlineExercise.onlineExercise import create_exercise, getexercise, gettheFile, stu_submit, getsubmission, \
    teagetsubmission, correct_exercise, getstusubmission, getstusubmissionname, gettheFile_name
from teacher.resourceManage import getfile
from teacher.resourceManage.resourceManage import getfilename

oe_bp=Blueprint('oe_bp',__name__,url_prefix='/oe')

from flask_cors import CORS  # 导入CORS库
CORS(oe_bp, supports_credentials=True)  # 启用CORS，允许跨域请求

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
    stuids = request.form.get('studentid_s')
    studentid_list = list(map(int, stuids.split(',')))
    # 这个file是一个特殊的数据结构，好像是从前端那里来的
    print(studentid_list)
    file_data = file.read()
    file_name=file.filename
    for stuid in studentid_list:
        create_exercise(teacherid,stuid,title,targetclass,file_data,file_name)
    return '文件上传成功'

@oe_bp.route('/uploadfromdb/', methods=['POST'])
def uploadfromdb():
    exeid=request.form.get('exeid')
    filecontent = getfile(exeid)
    file_name = getfilename(exeid)
    targetclass = request.form.get('targetclass')
    title = request.form.get('title')
    teacherid = request.form.get('teacherid')
    stuids = request.form.get('studentid_s')
    studentid_list = list(map(int, stuids.split(',')))
    # 这个file是一个特殊的数据结构，好像是从前端那里来的

    for stuid in studentid_list:
        create_exercise(teacherid,stuid,title,targetclass,filecontent,file_name)
    return '文件上传成功'

@oe_bp.route('/print/',methods=['POST'])
def homeprint():
    data = request.get_json()  # 获取 JSON 请求主体
    stuid = data.get('id')
    sqlresult = getexercise(stuid)
    result = [{
        "id":sqlresult[i]["id"],
        "teacher": sqlresult[i]["teacherid"],
        "title":sqlresult[i]["title"],
        "uploadTime":sqlresult[i]["createtime"],
        "exercisename": sqlresult[i]["exercisename"],
    } for i in range(len(sqlresult))]
    return jsonify(result)

@oe_bp.route('/download/', methods=['POST'])
def download():
    # request.get_json()和request.json一样，只是前者更加灵活，后者更加方便
    data = request.get_json()
    exercise = data.get('exercise')
    aimid = exercise['id']
    print(aimid)
    file_content = gettheFile(aimid)
    if file_content:
        return Response(
            file_content,
            mimetype='application/octet-stream',
            headers={"Content-Disposition": "attachment;filename=downloaded_file.ext"}
        )
    else:
        return "eaewaeResource not found", 404

@oe_bp.route('/raiseAnswer/', methods=['POST'])
def raiseAnswer():
    if 'file' not in request.files:
        return '没有选择文件', 400
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    aimid = request.form.get('exerciseId')
    print(aimid)
    # 这个file是一个特殊的数据结构，好像是从前端那里来的
    file_data = file.read()
    file_name = file.filename
    stu_submit(aimid, file_data,file_name)
    return '文件上传成功'

@oe_bp.route('/record/',methods=['POST'])
def historyprint():
    data = request.get_json()  # 获取 JSON 请求主体
    stuid = data.get('id')
    sqlresult = getsubmission(stuid)
    result = [{
        "id":sqlresult[i]["id"],
        "teacher": sqlresult[i]["teacherid"],
        "title": sqlresult[i]["title"],
        "submitTime":sqlresult[i]["submittime"],
        "checkTime":sqlresult[i]["correcttime"],
        "score": sqlresult[i]["grade"],
        "feedback": sqlresult[i]["feedback"],
    } for i in range(len(sqlresult))]
    return jsonify(result)

@oe_bp.route('/tearecord/',methods=['POST'])
def teahistoryprint():
    data = request.get_json()  # 获取 JSON 请求主体
    teaid = data.get('id')
    sqlresult = teagetsubmission(teaid)
    result = [{
        "id":sqlresult[i]["id"],
        "studentName": sqlresult[i]["studentid"],
        "title": sqlresult[i]["title"],
        "submitTime":sqlresult[i]["submittime"],
        "grade":sqlresult[i]["grade"],
        "correcttime": sqlresult[i]["correcttime"],
        "feedback": sqlresult[i]["feedback"],
        "answername": sqlresult[i]["answername"],
    } for i in range(len(sqlresult))]
    return jsonify(result)


@oe_bp.route('/correct/', methods=['POST'])
def correctfunc():
    aimid = request.form.get('aimid')
    score = request.form.get('score')
    comments = request.form.get('comments')
    # 这个file是一个特殊的数据结构，好像是从前端那里来的
    correct_exercise(score, comments, aimid)
    return '文件上传成功'

@oe_bp.route('/viewsubmission/', methods=['POST'])
def viewsubmission():
    # request.get_json()和request.json一样，只是前者更加灵活，后者更加方便
    data = request.get_json()
    record = data.get('record')
    aimid = record['id']
    file_content = getstusubmission(aimid)
    if file_content:
        return Response(
            file_content,
            mimetype='application/octet-stream',
            headers={"Content-Disposition": "attachment;filename=downloaded_file.ext"}
        )
    else:
        return "eaewaeResource not found", 404

@oe_bp.route('/preview_material/<int:file_id>', methods=['GET'])
def preview_material(file_id):
    file_content = getstusubmission(file_id)
    file_name=getstusubmissionname(file_id)
    if not file_content:
        return jsonify({"message": "Material not found"}), 404
    return send_file(
        io.BytesIO(file_content),
        download_name=file_name,
        as_attachment=False
    )

@oe_bp.route('/preview_material_stu/<int:file_id>', methods=['GET'])
def preview_material_stu(file_id):
    file_content = gettheFile(file_id)
    file_name=gettheFile_name(file_id)
    if not file_content:
        return jsonify({"message": "Material not found"}), 404
    return send_file(
        io.BytesIO(file_content),
        download_name=file_name,
        as_attachment=False
    )

