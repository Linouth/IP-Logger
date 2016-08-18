from sqlalchemy import Column, Integer, String
from .database import Base


class Picture(Base):
    __tablename__ = 'Pictures'
    id = Column(Integer, primary_key=True)
    filename = Column(String(5), unique=True)
    filetype = Column(String(5))
    visitors = Column(String)

    def __init__(self, filename, filetype, visitors='[]'):
        self.filename = filename
        self.filetype = filetype
        self.visitors = visitors

    def __repr__(self):
        return '<Picture %r>' % self.filename
