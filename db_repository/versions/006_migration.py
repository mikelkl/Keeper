from sqlalchemy import *
from migrate import *

from migrate.changeset import schema

pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
             Column('id', Integer, primary_key=True, nullable=False),
             Column('nickname', String(length=64)),
             Column('sex', String(length=5)),
             Column('age', String(length=5)),
             Column('height', String(length=8)),
             Column('weight', String(length=8)),
             Column('email', String(length=120)),
             Column('password', String(length=20)),
             Column('about_me', String(length=140)),
             Column('last_seen', DateTime),
             Column('avatar', String(length=40)),
             )


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['age'].create()
    post_meta.tables['user'].columns['height'].create()
    post_meta.tables['user'].columns['sex'].create()
    post_meta.tables['user'].columns['weight'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['age'].drop()
    post_meta.tables['user'].columns['height'].drop()
    post_meta.tables['user'].columns['sex'].drop()
    post_meta.tables['user'].columns['weight'].drop()
