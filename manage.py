#!flask/bin/python
# coding=utf8
import os
from app import create_app, db
from app.models import User, ECG, Treatment, Post

from flask.ext.migrate import Migrate, MigrateCommand, upgrade
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, ECG=ECG,
                Treatment=Treatment, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment tests."""

    # 把数据库迁移到最新修订版本
    upgrade()


if __name__ == '__main__':
    manager.run()
