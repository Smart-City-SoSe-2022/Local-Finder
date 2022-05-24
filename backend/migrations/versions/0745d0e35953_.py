"""empty message

Revision ID: 0745d0e35953
Revises: bcaf9cae5dc8
Create Date: 2022-05-18 18:36:58.293687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0745d0e35953'
down_revision = 'bcaf9cae5dc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('account_reservation_id_fkey', 'account', type_='foreignkey')
    op.drop_column('account', 'reservation_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('reservation_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('account_reservation_id_fkey', 'account', 'reservation', ['reservation_id'], ['id'])
    # ### end Alembic commands ###
