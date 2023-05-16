"""new table photos

Revision ID: eec9e131231c
Revises: 
Create Date: 2023-05-16 11:27:25.956481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eec9e131231c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "photos",
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("date_taken", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("path"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("photos")
    # ### end Alembic commands ###
