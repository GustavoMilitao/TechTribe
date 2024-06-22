# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0

"""init

Revision ID: 17ea75679da8
Revises:
Create Date: 2022-06-10 18:01:51.061536

"""


from alembic import op
import sqlalchemy as sa
import ormar
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "17ea75679da8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
            sa.Column("email", sa.String(length=100), nullable=False),
            sa.Column("username", sa.String(length=100), nullable=False),
            sa.Column("password", sa.String(length=100), nullable=False),
            sa.Column("verified", sa.Boolean(), nullable=True),
            sa.Column("verify_key", sa.String(length=100), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
            sa.UniqueConstraint("password"),
            sa.UniqueConstraint("username"),
            sa.UniqueConstraint("verify_key"),
        )
    if "quiz" not in tables:
        op.create_table(
            "quiz",
            sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
            sa.Column("public", sa.Boolean(), nullable=True),
            sa.Column("title", sa.String(length=100), nullable=False),
            sa.Column("description", sa.String(length=300), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.Column("user_id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True),
            sa.Column("questions", sa.JSON(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_quiz_users_id_user_id"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("id"),
        )
    if "user_sessions" not in tables:
        op.create_table(
            "user_sessions",
            sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
            sa.Column("user", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True),
            sa.Column("session_key", sa.String(length=64), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("ip_address", sa.String(length=100), nullable=True),
            sa.Column("user_agent", sa.String(length=255), nullable=True),
            sa.Column("last_seen", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(["user"], ["users.id"], name="fk_user_sessions_users_id_user"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("session_key"),
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_sessions")
    op.drop_table("quiz")
    op.drop_table("users")
    # ### end Alembic commands ###
