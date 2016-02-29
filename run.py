#!flask/bin/python

from app import app, db
from app.models import User, ECG, Treatment, Post

from flask.ext.script import Manager, Shell

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, ECG=ECG,
                Treatment=Treatment, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
