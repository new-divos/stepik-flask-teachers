"""empty message

Revision ID: 01b5d7118e11
Revises: b81f8679446f
Create Date: 2020-06-16 19:56:29.936764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01b5d7118e11'
down_revision = 'b81f8679446f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_table_rows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('slug', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('time')
    )
    op.create_table('time_table_columns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('time_table_cells',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('row_id', sa.Integer(), nullable=True),
    sa.Column('column_id', sa.Integer(), nullable=True),
    sa.Column('is_free', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['column_id'], ['time_table_columns.id'], ),
    sa.ForeignKeyConstraint(['row_id'], ['time_table_rows.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time_table_cells')
    op.drop_table('time_table_columns')
    op.drop_table('time_table_rows')
    # ### end Alembic commands ###