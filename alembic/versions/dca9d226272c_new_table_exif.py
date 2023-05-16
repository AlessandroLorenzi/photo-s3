"""new table exif

Revision ID: dca9d226272c
Revises: eec9e131231c
Create Date: 2023-05-16 12:06:16.879098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dca9d226272c"
down_revision = "eec9e131231c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "exifs",
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=True),
        sa.Column("make", sa.String(), nullable=True),
        sa.Column("iso", sa.Integer(), nullable=True),
        sa.Column("aperture", sa.Float(), nullable=True),
        sa.Column("shutter_speed", sa.Float(), nullable=True),
        sa.Column("exposure_bias", sa.Float(), nullable=True),
        sa.Column("exposure_program", sa.Integer(), nullable=True),
        sa.Column("rotation", sa.Integer(), nullable=True),
        sa.Column("date_taken", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("path"),
    )


def downgrade() -> None:
    op.drop_table("exifs")
