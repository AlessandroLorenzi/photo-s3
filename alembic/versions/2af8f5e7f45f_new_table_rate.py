"""new table rate

Revision ID: 2af8f5e7f45f
Revises: dca9d226272c
Create Date: 2023-05-16 14:14:09.086352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2af8f5e7f45f'
down_revision = 'dca9d226272c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rates',
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('path')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rates')
    # ### end Alembic commands ###
