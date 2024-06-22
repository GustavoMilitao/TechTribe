# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0

"""Added Backup-code

Revision ID: 901dfcdf8d38
Revises: 25f2c34a69c8
Create Date: 2022-12-18 11:48:22.772981

"""
import os

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import ormar

# revision identifiers, used by Alembic.
revision = "901dfcdf8d38"
down_revision = "25f2c34a69c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("backup_code", sa.String(length=64), nullable=True))
    conn = op.get_bind()
    session = Session(bind=conn)
    res = session.execute("SELECT id from users;")
    for row in res:
        user_id = str(row).strip(",.'()")
        session.execute(
            sa.sql.text("UPDATE users SET backup_code = :backup_code WHERE users.id=:user_id"),
            {"user_id": user_id, "backup_code": os.urandom(32).hex()},
        )
    op.alter_column("users", "backup_code", nullable=False)


# ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "backup_code")


# ### end Alembic commands ###
