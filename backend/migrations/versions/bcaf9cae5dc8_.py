"""empty message

Revision ID: bcaf9cae5dc8
Revises: 78cf570e3193
Create Date: 2022-05-18 18:31:35.312462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcaf9cae5dc8'
down_revision = '78cf570e3193'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('account_favorite_id_fkey', 'account', type_='foreignkey')
    op.drop_column('account', 'favorite_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('account_favorite_id_fkey', 'account', 'local', ['favorite_id'], ['id'])
    # ### end Alembic commands ###
