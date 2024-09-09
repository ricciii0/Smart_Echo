from mydatabase import db
class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    class_id=db.Column(db.String(20))