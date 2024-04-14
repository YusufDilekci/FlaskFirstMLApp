
from wtforms import Form, BooleanField, StringField, PasswordField, validators


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired(),])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])    