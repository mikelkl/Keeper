# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = 'app/static/uploads/avatars'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# mail server settings
MAIL_SERVER = 'smtp.sina.com'
MAIL_PORT = 465