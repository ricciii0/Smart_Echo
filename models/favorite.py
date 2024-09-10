from mydatabase import db

class Favorite(db.Model):
    __tablename__ = 'favorite'
    favorite_id = db.Column(db.String(30),nullable=False,primary_key=True,doc='收藏项id')
    user_id = db.Column(db.String(10), nullable=False, doc='用户id')
    title = db.Column(db.String(100), nullable=False,doc='标题')
    post_id = db.Column(db.String(20), nullable=False,doc='帖子id')
    favorite_time = db.Column(db.DateTime, nullable=False, doc='收藏时间')

    def to_dict(self):
        return {
            'favorite_id': self.favorite_id,
            'title': self.title,
            'post_id': self.post_id,
            'favorite_time': self.favorite_time,
            'user_id': self.user_id,
        }