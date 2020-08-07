"""empty message

Revision ID: bf0c78aca575
Revises: a8a965d2a8ea
Create Date: 2020-08-06 15:40:41.846737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf0c78aca575'
down_revision = 'a8a965d2a8ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('website', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
