from mydatabase import db

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.String(20), primary_key=True,doc='主题贴号')
    title = db.Column(db.String(100), nullable=False,doc='标题')
    poster_id = db.Column(db.String(10), nullable=False,doc='发布人账号')
    content = db.Column(db.Text, nullable=False,doc='内容')
    post_time = db.Column(db.DateTime, nullable=False,doc='主贴发布时间')
    likes_num = db.Column(db.Integer, nullable=False, doc='点赞数')
    favorites_num = db.Column(db.Integer, nullable=False,doc='收藏量')
    dislikes_num = db.Column(db.Integer, nullable=False,doc='不赞成数')
    replies_num = db.Column(db.Integer,nullable=False,doc='评论数量')

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'title': self.title,
            'poster_id': self.poster_id,
            'content': self.content,
            'post_time': self.post_time,
            'likes_num': self.likes_num,
            'favorites_num': self.favorites_num,
            'dislikes_num': self.dislikes_num,
            'replies_num': self.replies_num,
        }
