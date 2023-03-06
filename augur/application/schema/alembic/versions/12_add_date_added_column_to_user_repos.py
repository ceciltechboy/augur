"""Add date added column to user repos

Revision ID: 12
Revises: 11
Create Date: 2023-03-03 18:27:06.103445

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '12'
down_revision = '11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_repos', sa.Column('date_added', postgresql.TIMESTAMP(precision=0), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False), schema='augur_operations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_repos', 'date_added', schema='augur_operations')
    # ### end Alembic commands ###
