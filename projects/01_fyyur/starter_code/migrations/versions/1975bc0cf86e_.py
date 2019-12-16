"""empty message

Revision ID: 1975bc0cf86e
Revises: f283bd226cc9
Create Date: 2019-12-14 16:47:27.790129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1975bc0cf86e'
down_revision = 'f283bd226cc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('show', 'start_time')
    # ### end Alembic commands ###