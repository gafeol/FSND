"""empty message

Revision ID: 1b3e757d8bd4
Revises: f58d9b4652e2
Create Date: 2020-08-04 14:54:43.469053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b3e757d8bd4'
down_revision = 'f58d9b4652e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('website', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###