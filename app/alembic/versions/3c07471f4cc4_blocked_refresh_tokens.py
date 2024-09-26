"""blocked_refresh_tokens

Revision ID: 3c07471f4cc4
Revises: 16e36c4a37f4
Create Date: 2024-09-26 14:45:02.758637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c07471f4cc4'
down_revision = '16e36c4a37f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocked_refresh_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('refresh_token', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('refresh_token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blocked_refresh_tokens')
    # ### end Alembic commands ###
