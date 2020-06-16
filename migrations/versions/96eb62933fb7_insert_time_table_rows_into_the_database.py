"""Insert time table rows into the database

Revision ID: 96eb62933fb7
Revises: 726ee7a435aa
Create Date: 2020-06-16 21:02:09.309794

"""
from datetime import time

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision = '96eb62933fb7'
down_revision = '726ee7a435aa'
branch_labels = None
depends_on = None

Base = declarative_base()


class TimeTableRow(Base):
    __tablename__ = 'time_table_rows'

    id = sa.Column('id', sa.Integer, primary_key=True)
    time = sa.Column('time', sa.Time, unique=True)
    slug = sa.Column('slug', sa.String(5), unique=True)


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for id, hour in enumerate(range(8, 23, 2), 1):
        row = TimeTableRow(
            id=id,
            time=time(hour=hour),
            slug=str(hour)
        )
        session.add(row)

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for row in session.query(TimeTableRow).all():
        session.delete(row)

    session.commit()
