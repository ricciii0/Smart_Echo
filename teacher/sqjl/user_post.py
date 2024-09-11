from flask import Flask, request, jsonify,make_response
from models.post import Post
from mydatabase import db

def create_posts():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['title', 'poster_id', 'content', 'post_time']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    count = 0
    posts = Post.query.all()
    if posts:
        count = len(posts)
    new_post = Post(
        post_id=data['poster_id'] + '_' + str(count+1),

        title=data['title'],
        poster_id=data['poster_id'],
        content=data['content'],
        post_time=data['post_time'],

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
        return jsonify({"error": "No data provided"}), 400
    post_id = data['post_id']
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    else:
        return jsonify({'error': 'Post not found'}), 404

def get_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    required_fields = ['post_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    post = Post.query.get(data['post_id'])
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({'error': 'Post not found'}), 404

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
        return jsonify({"error": "No data provided"}), 400
    post_id = data['post_id']
    if not post_id:
        return jsonify({"error": "No user_id provided"}), 400
    post = Post.query.get(post_id)
    post.likes_num += 1
    db.session.commit()
    return jsonify({'message': 'Post liked successfully'}), 201
