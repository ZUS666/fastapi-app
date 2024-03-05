"""init.

Revision ID: ea96995b71e1
Revises: 
Create Date: 2024-03-05 21:55:59.007729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea96995b71e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # added server_default to is_active, is_admin and email_regex constraint
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), sa.Identity(always=True, cycle=True), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False, comment='User email'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='User is active status', server_default='FALSE'),
    sa.Column('is_admin', sa.Boolean(), nullable=False, comment='User is admin status', server_default='FALSE'),
    sa.Column('password', sa.String(length=256), nullable=False, comment='User password'),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_check_constraint(
        'email_regex',
        'users',
        "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}$'",
    )
    op.create_table('profiles',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    op.drop_table('users')
    # ### end Alembic commands ###
