from mydatabase import db
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGBLOB

class AnswerFile(db.Model):
    __tablename__ = 'answerfiles'
    file_id = db.Column(db.String(10), primary_key=True)
    file_name = db.Column(db.String(20), nullable=False)
    file_content = db.Column(LONGBLOB, nullable=True)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(10), nullable=False)
    question_id = db.Column(db.String(20), nullable=False)
    def to_dict(self):
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'file_content': self.file_content,
            'upload_time': self.upload_time,
            'user_id': self.user_id,
            'question_id': self.question_id,
        }