from mydatabase import db
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class TeachingFile(db.Model):
    __tablename__ = 'teachingfiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(25), nullable=True)
    filecontent = Column(LONGBLOB, nullable=False)
    subject = Column(String(25), nullable=True)
    uploadtime = Column(DateTime, default=datetime.utcnow)
