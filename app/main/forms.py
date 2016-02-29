# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class EditProfileForm(Form):
    nickname = StringField(validators=[Length(0, 64)])
    about_me = TextAreaField()
    submit = SubmitField('保存修改'.decode('utf8'))
