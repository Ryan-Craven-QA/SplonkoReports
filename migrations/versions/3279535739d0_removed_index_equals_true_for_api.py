"""removed index equals true for API

Revision ID: 3279535739d0
Revises: f2bdd691b842
Create Date: 2021-06-25 10:04:00.093041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3279535739d0'
down_revision = 'f2bdd691b842'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_api_apidata', table_name='api')
    op.drop_index('ix_api_apiname', table_name='api')
    op.drop_index('ix_api_apiurl', table_name='api')
    op.drop_index('ix_api_requesttype', table_name='api')
    op.create_unique_constraint(None, 'api', ['apiname'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'api', type_='unique')
    op.create_index('ix_api_requesttype', 'api', ['requesttype'], unique=False)
    op.create_index('ix_api_apiurl', 'api', ['apiurl'], unique=False)
    op.create_index('ix_api_apiname', 'api', ['apiname'], unique=False)
    op.create_index('ix_api_apidata', 'api', ['apidata'], unique=False)
    # ### end Alembic commands ###
