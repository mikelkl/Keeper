# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    email = StringField(validators=[Required(), Length(1, 64), Email()])
    password = PasswordField(validators=[Required()])
    remember_me = BooleanField()
    submit = SubmitField('登陆'.decode('utf8'))


class EditProfileForm(Form):
    nickname = StringField(validators=[Length(0, 64)])
    about_me = TextAreaField()
    submit = SubmitField('保存修改'.decode('utf8'))
