# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0

"""Added kahoot_id

Revision ID: 7ad8502af419
Revises: 820e06ef2c2a
Create Date: 2023-01-27 22:30:00.331395

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = "7ad8502af419"
down_revision = "820e06ef2c2a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("quiz", sa.Column("kahoot_id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("quiz", "kahoot_id")
    # ### end Alembic commands ###
