from flask import Flask, request, jsonify
from models.question import Question
from mydatabase import db

def create_questions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['student_id', 'question', 'subject']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    count = 0
    questions = Question.query.all()
    if questions:
        count =len(questions)
    new_question = Question(
        question_id=data['student_id'] + '_' + str(count+1),
        student_id=data['student_id'],
        question=data['question'],
        subject=data['subject'],
        answer='',
        is_answer=False,
        teacher_id='',
        answer_time='',
    )
    db.session.add(new_question)
    db.session.commit()

    return jsonify(new_question.to_dict()), 201


def get_questions():
    questions = Question.query.filter(Question.is_answer == False).all()
    return jsonify([q.to_dict() for q in questions]), 200

def get_question():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    question_id = data['question_id']
    question = Question.query.get(question_id)
    return jsonify(question.to_dict()), 200

def answer_questions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    question_id = data['question_id']
    teacher_id = data['teacher_id']
    answer_content = data['answer']
    answer_time = data['answer_time']
    if not answer_content:
        return jsonify({'error': '解答内容不能为空'}), 400
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': '未找到该问题'}), 404

    question.answer = answer_content
    question.is_answer = True
    question.teacher_id = teacher_id
    question.answer_time = answer_time

    db.session.commit()

    return jsonify({'message': '问题解答成功', 'question_id': question_id}), 200


def get_answers():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    question_id = data['question_id']
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': '未找到该问题'}), 404

    if not question.is_answer:
        return jsonify({"message":"暂无答案，请等待老师解答"}),201

    return jsonify(question.to_dict()), 200


def delete_questions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    question_id = data['question_id']
    question = Question.query.get(question_id)
    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message': 'Question deleted successfully'}), 200
    else:
        return jsonify({'error': 'Question not found'}), 404