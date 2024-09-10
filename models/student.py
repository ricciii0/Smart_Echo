from mydatabase import db
class Student(db.Model):
    user_id = db.Column(db.String(9),db.ForeignKey('user.user_id'), primary_key=True)
    class_id=db.Column(db.String(20))