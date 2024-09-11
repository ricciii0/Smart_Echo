from flask import Flask, request, jsonify
from models.reply import Reply
from models.post import Post
from mydatabase import db


def create_replies():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['content','publisher_id', 'post_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    count = 0
    replies = Reply.query.filter(Reply.post_id == data['post_id']).all()
    if replies:
        count = len(replies)

    new_reply = Reply(
        reply_id = data['post_id']+'_'+str(count+1),
        publisher_id = data['publisher_id'],
        content=data['content'],
        post_id=data['post_id'],

        likes_num = 0,
        dislikes_num = 0,
        replies_num = 0,
    )
    post =  Post.query.get(data['post_id'])
    post.replies_num += 1

    db.session.add(new_reply)
    db.session.commit()

    return jsonify(new_reply.to_dict()), 201


def delete_replies():
    data = request.get_json()
    reply_id = data['reply_id']
    reply = Reply.query.get(reply_id)

    if reply:
        db.session.delete(reply)
        db.session.commit()
        return jsonify({'message': 'Reply deleted successfully'}), 200
    else:
        return jsonify({'error': 'Reply not found'}), 404


def get_replies():
    post_id = request.args.get('post_id')
    replies = Reply.query.filter(Reply.post_id==post_id).all()
    return jsonify([r.to_dict() for r in replies]), 200
