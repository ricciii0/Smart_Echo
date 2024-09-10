from mydatabase import db

class Reply(db.Model):
    __tablename__ = 'replies'
    reply_id = db.Column(db.String(30),nullable=False,primary_key=True,doc='回复号')
    publisher_id = db.Column(db.String(10), nullable=False, doc='发布人账号')
    content = db.Column(db.Text, nullable=False,doc='内容')
    reply_time = db.Column(db.DateTime, nullable=False,doc='回复发布时间')

    likes_num = db.Column(db.Integer, nullable=False, doc='点赞数')
    dislikes_num = db.Column(db.Integer, nullable=False, doc='不赞成数')
    replies_num = db.Column(db.Integer, nullable=False, doc='评论数量')
    post_id = db.Column(db.String(20), nullable=False, doc='主题贴号')

    def to_dict(self):
        return {
            'reply_id': self.reply_id,

            'publisher_id': self.publisher_id,
            'content': self.content,
            'reply_time': self.reply_time,

            'likes_num': self.likes_num,
            'dislikes_num': self.dislikes_num,
            'replies_num': self.replies_num,
            'post_id': self.post_id,
        }