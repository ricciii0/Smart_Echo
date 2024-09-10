from mydatabase import db
class Teacher(db.Model):
    user_id=db.Column(db.String(9),db.ForeignKey('user.user_id'),primary_key=True)
    subject=db.Column(db.String(50))
    class1=db.Column(db.String(50))
    class2=db.Column(db.String(50))