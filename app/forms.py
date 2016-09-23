from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class RegisterForm(FlaskForm):
    username = StringField('Username', [
        validators.Length(min=3, max=25,
                          message='Username should be 3 to 25 characters long.'),
        validators.DataRequired(message='Username missing')
    ])
    email = StringField('Email', [
        validators.Email(),
        validators.DataRequired(message='Email missing')
    ])
    invite_key = StringField('Invite Key', [
        validators.length(min=10, max=10,
                          message='Invite key should be 10 characters long.'),
        validators.DataRequired(message='Invite Key missing')
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(message='Password missing.'),
        validators.EqualTo('confirm', message='Passwords must match.')
    ])
    confirm = PasswordField('Repeat Password')
    # TODO: TOS ?


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Your Password')
