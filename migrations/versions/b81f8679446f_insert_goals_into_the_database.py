"""Insert goals into the database

Revision ID: b81f8679446f
Revises: b48ce44980a5
Create Date: 2020-06-15 17:32:14.921740

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from data import goals


# revision identifiers, used by Alembic.
revision = 'b81f8679446f'
down_revision = 'b48ce44980a5'
branch_labels = None
depends_on = None


Base = declarative_base()


class Goal(Base):
    __tablename__ = 'goals'

    id = sa.Column('id', sa.Integer, primary_key=True)
    code = sa.Column('code', sa.String(15), unique=True)
    title = sa.Column('title', sa.String(70), nullable=False)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    goals_lst = list(goals.items())
    goals_lst.sort(key=lambda item: item[1])
    for code, title in goals_lst:
        session.add(Goal(code=code, title=title))

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for code in goals.keys():
        goal = session.query(Goal).filter(Goal.code == code).first()
        if goal is not None:
            session.delete(goal)

    session.commit()
