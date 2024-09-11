from datetime import datetime
from mydatabase import db

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teaid = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(25, collation='utf8mb4_general_ci'), nullable=True)
    filecontent = db.Column(db.LargeBinary, nullable=False)
    subject = db.Column(db.String(25), nullable=True)
    uploadtime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<File {self.filename}>'