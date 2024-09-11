import random
import string
from datetime import datetime

from flask import Flask, request, jsonify,make_response
from models.post import Post
from mydatabase import db

def create_posts():
    data = request.get_json()
    if not data:
        return jsonify({"error": "未提供指定数据"}), 400

    required_fields = ['title', 'poster_id', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "关键数据缺失"}), 400

    count = 0
    posts = Post.query.all()
    if posts:
        count = len(posts)
    random_chars = ''.join(random.choice(string.ascii_letters) for _ in range(4))
    new_post = Post(
        post_id=data['poster_id'] + '_' + random_chars + "_" + str(count+1),

        title=data['title'],
        poster_id=data['poster_id'],
        content=data['content'],

        likes_num = 0,
        dislikes_num = 0,
        favorites_num = 0,
        replies_num = 0,
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201


def delete_posts():
    data = request.get_json()
    if not data:
        return jsonify({"error": "未提供指定数据"}), 400
    post_id = data['post_id']
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': '帖子成功删除'}), 200
    else:
        return jsonify({'error': '找不到帖子'}), 404

def get_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "未提供指定数据"}), 400
    required_fields = ['post_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "关键数据缺失"}), 400
    post = Post.query.get(data['post_id'])
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({'error': '找不到帖子'}), 404

def get_posts_by_likes():
    order = request.args.get('order', 'asc')
    limit = int(request.args.get('limit', 10))
    query = Post.query.order_by(Post.likes_num.asc() if order == 'asc' else Post.likes_num.desc()).limit(limit)
    posts = query.all()
    return jsonify([post.to_dict() for post in posts])


def get_posts_by_favorites():
    order = request.args.get('order', 'asc')
    limit = int(request.args.get('limit', 10))
    query = Post.query.order_by(Post.favorites_num.asc() if order == 'asc' else Post.favorites_num.desc()).limit(limit)
    posts = query.all()
    return jsonify([post.to_dict() for post in posts])

def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

def add_likes_num():
    data = request.get_json()
    if not data:
        return jsonify({"error": "未提供指定数据"}), 400
    post_id = data['post_id']
    if not post_id:
        return jsonify({"error": "未提供post_id"}), 400
    post = Post.query.get(post_id)
    post.likes_num += 1
    db.session.commit()
    return jsonify({'message': '点赞成功'}), 201
