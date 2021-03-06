"""add cleanleave model

Revision ID: e5e8536ff3d5
Revises: 341249956d89
Create Date: 2022-01-24 16:48:21.814329

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e5e8536ff3d5"
down_revision = "341249956d89"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "joinmessages",
        sa.Column("id_slug", sa.String(length=255), nullable=False),
        sa.Column("channel_id", sa.BigInteger(), nullable=False),
        sa.Column("message_id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id_slug"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("joinmessages")
    # ### end Alembic commands ###
