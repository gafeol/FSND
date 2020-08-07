"""empty message

Revision ID: 72f5d99ebe2f
Revises: b53645da3892
Create Date: 2020-08-06 20:31:25.277913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72f5d99ebe2f'
down_revision = 'b53645da3892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
