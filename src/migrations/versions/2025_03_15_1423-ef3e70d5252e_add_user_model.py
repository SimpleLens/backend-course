"""add user model

Revision ID: ef3e70d5252e
Revises: 3f86f1a5b9e7
Create Date: 2025-03-15 14:23:44.628740

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ef3e70d5252e"
down_revision: Union[str, None] = "3f86f1a5b9e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("username", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    op.drop_table("users")
