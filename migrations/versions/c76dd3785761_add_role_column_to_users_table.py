"""Add role column to users table

Revision ID: c76dd3785761
Revises: b5bf8dbfda4c
Create Date: 2024-07-29 20:37:05.627396

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine


# revision identifiers, used by Alembic.
revision = 'c76dd3785761'
down_revision = 'b5bf8dbfda4c'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
      with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=False, server_default='patient'))
    # Note: Removed the line to drop the default value constraint due to SQLite limitations
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
