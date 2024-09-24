"""create notes tasks tables

Revision ID: 3912777f2186
Revises: 
Create Date: 2024-09-25 01:52:40.006188

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3912777f2186"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("content", sa.String(length=50000), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notes")),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=50000), nullable=True),
        sa.Column("priority", sa.String(length=15), nullable=True),
        sa.Column("deadline_at", sa.DateTime(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("notes")
