"""empty message

Revision ID: 77059b95272d
Revises: 9c71552acfd0
Create Date: 2022-06-19 17:41:48.125269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77059b95272d'
down_revision = '9c71552acfd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lokal', sa.Column('address', sa.String(), nullable=True))
    op.add_column('lokal', sa.Column('plz', sa.String(), nullable=True))
    op.add_column('lokal', sa.Column('city', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lokal', 'city')
    op.drop_column('lokal', 'plz')
    op.drop_column('lokal', 'address')
    # ### end Alembic commands ###
