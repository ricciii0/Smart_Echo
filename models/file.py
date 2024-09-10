from mydatabase import db
import datetime
from enum import Enum

class FileType(Enum):
    TXT="txt"
    MD="md"
    PDF="pdf"

class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    filename = db.Column(db.String(20), nullable=False)
    file_type = db.Column(db.Enum(FileType), nullable=False)
    subject=db.Column(db.String(20), nullable=False)
    upload_ime=db.Column(db.DateTime, unique=True, nullable=datetime.datetime.now())