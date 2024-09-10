from flask import Flask, request, jsonify
from teacher import community_blueprint
from teacher.sqjl.user_question import create_questions,get_questions,get_answers,delete_questions,answer_questions,get_question
from teacher.sqjl.user_post import (create_posts,delete_posts,get_posts_by_likes,
                       get_posts_by_favorites,get_post, get_posts, add_likes_num)
from teacher.sqjl.user_reply import create_replies,delete_replies,get_replies
from teacher.sqjl.user_favorite import (add_favorite,delete_favorite,get_favorite, is_favorite)
from flask_cors import CORS  # 导入CORS库


CORS(community_blueprint, supports_credentials=True)  # 启用CORS，允许跨域请求

@community_blueprint.route('/create_posts',methods=['POST'])
def create__posts():
    return create_posts()

@community_blueprint.route('/delete_posts',methods=['DELETE'])
def delete__posts():
    return delete_posts()

@community_blueprint.route('/get_posts_by_likes', methods=['GET'])
def get__posts_by_likes():
    return get_posts_by_likes()

@community_blueprint.route('/get_posts_by_favorites', methods=['GET'])
def get__posts_by_favorites():
    return get_posts_by_favorites()

@community_blueprint.route('/get_post',methods=['GET'])
def get__post():
    return get_post()

@community_blueprint.route('/get_posts', methods=['GET'])
def get__posts():
    return get_posts()

@community_blueprint.route('/add_likes_num', methods=['POST'])
def add__likes_num():
    return add_likes_num()


@community_blueprint.route('/create_replies',methods=['POST'])
def create__replies():
    return create_replies()

@community_blueprint.route('/delete_replies',methods=['DELETE'])
def delete__replies():
    return delete_replies()

@community_blueprint.route('/get_replies', methods=['GET'])
def get__replies():
    return get_replies()


@community_blueprint.route('/create_questions', methods=['POST'])
def create__questions():
    return create_questions()

@community_blueprint.route('/get_questions', methods=['GET'])
def get__questions():
    return get_questions()

@community_blueprint.route('/get_question',methods=['GET'])
def get__question():
    return get_question()

@community_blueprint.route('/get_answers', methods=['GET'])
def get__answers():
    return get_answers()

@community_blueprint.route('/delete_questions',methods=['DELETE'])
def delete__questions():
    return delete_questions()

@community_blueprint.route('/answer_questions',methods=['POST'])
def answer__questions():
    return answer_questions()



@community_blueprint.route('/delete_favorite', methods=['DELETE'])
def delete__favorite():
    return delete_favorite()

@community_blueprint.route('/get_favorite',methods=['GET'])
def get__favorite():
    return get_favorite()

@community_blueprint.route('/add_favorite',methods=['POST'])
def add__favorite():
    return add_favorite()

@community_blueprint.route('/is_favorite', methods=['GET'])
def is__favorite():
    return is_favorite()