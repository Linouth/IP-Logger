from .database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class Picture(Base):
    __tablename__ = 'Pictures'
    id = Column(Integer, primary_key=True)
    filename = Column(String(5), unique=True, index=True)
    filetype = Column(String(5))
    visitors = Column(String)
    uploaded_by = Column(String(25), index=True)

    def __init__(self, filename, filetype, uploaded_by, visitors='[]'):
        self.filename = filename
        self.filetype = filetype
        self.uploaded_by = uploaded_by
        self.visitors = visitors

    def __repr__(self):
        return '<Picture %r>' % self.filename


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, index=True)
    password = Column(String)
    email = Column(String(50), unique=True, index=True)
    registered_on = Column(DateTime)
    ip = Column(String(46))
    invite_key = Column(String(10))
    privileges = Column(Integer)

    def __init__(self, username, password, email, ip, invite_key, priv=0):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.ip = ip
        self.invite_key = invite_key
        self.priv = priv

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class Invite(Base):
    __tablename__ = 'Invites'
    id = Column(Integer, primary_key=True)
    invite_key = Column(String(10), unique=True, index=True)
    available = Column(Boolean())
    privileges = Column(Integer)

    def __init__(self, invite, priv=0):
        self.invite_key = invite
        self.privileges = priv
        self.available = True

    def __repr__(self):
        return '<Invite %r>' % self.invite
