"""add guild models

Revision ID: fb0890cc55c9
Revises: e67e9b1eb8f5
Create Date: 2022-01-22 15:57:10.505973

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "fb0890cc55c9"
down_revision = "e67e9b1eb8f5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "guilds",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("banned", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "guildconfigs",
        sa.Column("guild", sa.BigInteger(), nullable=True),
        sa.Column("service", sa.String(length=255), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["guild"], ["guilds.id"], name="fk_guildconfigs_guilds_id_guild"),
        sa.PrimaryKeyConstraint("service"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("guildconfigs")
    op.drop_table("guilds")
    # ### end Alembic commands ###
