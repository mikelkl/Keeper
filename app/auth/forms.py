# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    email = StringField(validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(validators=[Required()])
    remember_me = BooleanField()
    submit = SubmitField('登陆'.decode('utf8'))
