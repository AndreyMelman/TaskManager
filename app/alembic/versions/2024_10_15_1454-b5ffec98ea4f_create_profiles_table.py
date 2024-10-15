"""create profiles table

Revision ID: b5ffec98ea4f
Revises: 0d32a7999e5b
Create Date: 2024-10-15 14:54:21.501613

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b5ffec98ea4f"
down_revision: Union[str, None] = "0d32a7999e5b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=True),
        sa.Column("last_name", sa.String(length=32), nullable=True),
        sa.Column("bio", sa.String(length=5000), nullable=True),
        sa.Column("phone_number", sa.String(length=32), nullable=True),
        sa.Column("address", sa.String(length=64), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_profiles_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_profiles")),
        sa.UniqueConstraint("user_id", name=op.f("uq_profiles_user_id")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("profiles")
    # ### end Alembic commands ###