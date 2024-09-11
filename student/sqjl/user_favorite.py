from flask import Flask, request, jsonify
from models.favorite import Favorite
from models.post import Post
from sqlalchemy import and_
from mydatabase import db


def add_favorite():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['user_id','title','post_id']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    count = 0
    favorite = Favorite.query.filter(Favorite.user_id == data['user_id']).all()
    if favorite:
        count = len(favorite)

    new_favorite = Favorite(
        title=data['title'],
        post_id=data['post_id'],
        user_id=data['user_id'],
        favorite_id = data['user_id']+"_"+data['post_id'],
    )
    post = Post.query.get(data['post_id'])
    if post:
        post.favorites_num += 1
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.to_dict()), 201


def delete_favorite():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    post_id = data['post_id']
    user_id = data['user_id']
    post = Post.query.get(post_id)
    favorite = Favorite.query.filter(and_(Favorite.post_id == post_id, Favorite.user_id == user_id)).first()
    if favorite:
        post.favorites_num -= 1
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite deleted successfully'}), 200
    else:
        return jsonify({'error': 'Favorite not found'}), 404


def get_favorite():
    user_id = request.args.get('user_id')
    favorites = Favorite.query.filter(Favorite.user_id == user_id).all()
    if favorites:
        return jsonify([favorite.to_dict() for favorite in favorites]), 200
    else:
        return jsonify({'error': 'Favorite not found'}), 404

def is_favorite():
    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')
    favorites = Favorite.query.filter(Favorite.user_id == user_id).all()
    if favorites:
        for favorite in favorites:
            if favorite.post_id == post_id:
                return jsonify({'is_favorite':  True}), 200
    return {"is_favorite": False}