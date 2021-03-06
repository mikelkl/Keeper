"""empty message

Revision ID: d2225df93049
Revises: 0b9b86c3f000
Create Date: 2016-03-01 16:30:01.915000

"""

# revision identifiers, used by Alembic.
revision = 'd2225df93049'
down_revision = '0b9b86c3f000'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.drop_index('ix_user_password', table_name='user')
    op.drop_column('user', 'password')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=20), nullable=True))
    op.create_index('ix_user_password', 'user', ['password'], unique=False)
    op.drop_column('user', 'password_hash')
    ### end Alembic commands ###
