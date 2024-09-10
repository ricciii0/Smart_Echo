from mydatabase import db

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.String(10), primary_key=True,doc='问题号')
    student_id = db.Column(db.String(10), nullable=False,doc='发布同学账号')
    question = db.Column(db.Text, nullable=False,doc='问题内容')
    subject = db.Column(db.String(10),nullable=False,doc='所属科目')
    question_time = db.Column(db.DateTime, nullable=False,doc='问题发布时间')
    answer = db.Column(db.Text,nullable=True,doc='解答内容')
    is_answer = db.Column(db.Boolean, nullable=False, default=False,doc='是否被解答')
    teacher_id = db.Column(db.String(10), nullable=True,doc='回答老师账号')
    answer_time = db.Column(db.DateTime, nullable=True, doc='问题解答时间')

    def to_dict(self):
        return {
            'question_id': self.question_id,
            'student_id': self.student_id,
            'question': self.question,
            'subject': self.subject,
            'question_time': self.question_time,
            'answer': self.answer,
            'is_answer': self.is_answer,
            "teacher_id": self.teacher_id,
            'answer_time': self.answer_time,
        }