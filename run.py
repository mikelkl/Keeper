#!flask/bin/python

from app import app, db
from app.models import User, ECG, Treatment, Post

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, ECG=ECG,
                Treatment=Treatment, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
