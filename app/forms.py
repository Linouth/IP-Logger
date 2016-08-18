from . import get_db
import datetime
from flask import flash
from wtform import Form, StringField, PasswordField, validators


class User:
    def __init__(self, username, password, email=None, ip=None):
        self.username = username
        self.password = password
        if email is None:
            # Login
            if self.__login(username, password):
                self.authenticated = True
            else:
                self.authenticated = False
        else:
            # Register
            self.email = email
            self.registered_on = datetime.utcnow()
            self.ip = ip
            self.__register()

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_dict(self):
        return dict(
                username=self.username,
                password=self.password,
                email=self.email,
                ip=self.ip,
                registered_on=self.registered_on
        )

    def __login(self, username, password):
        db = get_db()
        cur = db.execute('select * from Users where username=? and password=?',
                         (username, password))
        user = cur.fetchone()
        if user is None:
            # flash('Username or Password is invalid', 'error')
            return False
        self.id = user['id']
        self.email = user['email']
        self.registered_on = user['registered_on']
        self.ip = user['ip']
        return True

    def __register(self, username, password, email, ip):
        db = get_db()
        db.execute('insert into Users (username, email, password,\
                                       registered_on, ip) values \
                    (:username, :email, :password, :registered_on, :ip)',
                   self.get_dict())
        db.commit()


class RegisterForm(Form):
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.DataRequired()
    ])
    email = StringField('Email', [
        validators.Length(min=6, max=35),
        validators.DataRequired()
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualsTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # TODO: TOS ?


class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Your Password')
