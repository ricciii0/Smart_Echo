from mydatabase import db
class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    subject=db.Column(db.String(50))
    class1=db.Column(db.String(50))
    class2=db.Column(db.String(50))