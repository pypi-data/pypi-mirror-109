"""Add markers and extra needed for resolver

Revision ID: f60593780969
Revises: 1ee67d9a7861
Create Date: 2019-10-02 20:04:59.209567+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f60593780969"
down_revision = "1ee67d9a7861"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("depends_on", sa.Column("extra", sa.String(length=256), nullable=True))
    op.add_column("depends_on", sa.Column("marker", sa.String(length=256), nullable=True))
    op.add_column("depends_on", sa.Column("marker_evaluation_result", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("depends_on", "marker_evaluation_result")
    op.drop_column("depends_on", "marker")
    op.drop_column("depends_on", "extra")
    # ### end Alembic commands ###
