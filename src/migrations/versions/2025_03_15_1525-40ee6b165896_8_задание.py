"""8 задание

Revision ID: 40ee6b165896
Revises: ef3e70d5252e
Create Date: 2025-03-15 15:25:24.356092

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "40ee6b165896"
down_revision: Union[str, None] = "ef3e70d5252e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("email", "users", ["email"])
    op.create_unique_constraint("username", "users", ["username"])


def downgrade() -> None:
    op.drop_constraint("email", "users", type_="unique")
    op.drop_constraint("username", "users", type_="unique")
