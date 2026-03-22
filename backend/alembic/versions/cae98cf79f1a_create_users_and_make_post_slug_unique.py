"""create users and make post slug unique

Revision ID: cae98cf79f1a
Revises: 68cbb8474aaa
Create Date: 2026-03-22 11:10:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cae98cf79f1a"
down_revision: Union[str, Sequence[str], None] = "68cbb8474aaa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.drop_index(op.f("ix_posts_slug"), table_name="posts")
    op.create_index(op.f("ix_posts_slug"), "posts", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_posts_slug"), table_name="posts")
    op.create_index(op.f("ix_posts_slug"), "posts", ["slug"], unique=False)

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
