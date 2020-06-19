#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from flask.cli import FlaskGroup, AppGroup
from flask_migrate import Migrate
from mimesis import Person

from app import create_app, db
from app.models import (
    ClientRequest,
    Goal,
    Teacher,
    TimeTableCell,
    TimeTableColumn,
    TimeTableRow,
)
from config import config
from data import Possibility


current_config = config.get(os.getenv('FLASK_ENV'))
if current_config is None:
    raise RuntimeError(
        "Unknown configuration: check FLASK_ENV environment variable value"
    )

app = create_app(current_config)
migrate = Migrate(app, db)
cli = FlaskGroup(app)


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        ClientRequest=ClientRequest,
        Goal=Goal,
        Teacher=Teacher,
        TimeTableCell=TimeTableCell,
        TimeTableColumn=TimeTableColumn,
        TimeTableRow=TimeTableRow,
        Possibility=Possibility,
    )


data_cli = AppGroup('data')
app.cli.add_command(data_cli)


@data_cli.command('add')
def append_data():
    from data import get_current_week, teachers, weekdays

    week = get_current_week()

    goals = dict()
    for goal in db.session.query(Goal).all():
        goals[goal.code] = goal

    time_points = dict()
    for row in db.session.query(TimeTableRow):
        time_points[row.time.strftime('%H:%M').lstrip('0')] = row.id

    person = Person('ru')

    for teacher in teachers:
        id = teacher.get('id', -1)
        if id < 0:
            logging.warning(f"Illegal teacher identifier {id}")
            continue

        teacher_obj = db.session.query(Teacher).filter(
            Teacher.id == id
        ).first()
        if teacher_obj is None:
            name = teacher.get('name')
            if not name:
                logging.warning(f"Illegal teacher name (id={id})")

            price = float(teacher.get('price', 0))
            if price <= 0.0:
                logging.warning(f"Illegal teacher price (id={id})")

            teacher_obj = Teacher(
                id=id,
                name=name,
                rating=teacher.get('rating', 0.0),
                price=price,
            )

            about = teacher.get('about')
            if about:
                teacher_obj.about = about

            picture = teacher.get('picture')
            if picture:
                teacher_obj.picture = picture

            for goal in teacher.get('goals', []):
                goal_obj = goals.get(goal)
                if goal_obj is not None:
                    teacher_obj.goals.append(goal_obj)

            db.session.add(teacher_obj)

            time_table = teacher.get('free', dict())
            for i, time_table_date in enumerate(week):
                column_obj = TimeTableColumn(
                    teacher=teacher_obj,
                    date=time_table_date
                )
                db.session.add(column_obj)

                time_table_day = time_table.get(weekdays[i].code, dict())
                if time_table_day:
                    for time_key, is_free in time_table_day.items():
                        row_id = time_points.get(time_key)
                        if row_id is not None:
                            cell_obj = TimeTableCell(
                                is_free=is_free,
                                row_id=row_id,
                                column=column_obj
                            )

                            if not is_free:
                                cell_obj.name = person.full_name()
                                cell_obj.phone = person.telephone()

                            db.session.add(cell_obj)

                        else:
                            logging.warning(f"Illegal time key {time_key}")

                else:
                    for row_id in time_points.values():
                        cell_obj = TimeTableCell(
                            is_free=True,
                            row_id=row_id,
                            column=column_obj
                        )
                        db.session.add(cell_obj)

    # noinspection PyBroadException
    try:
        db.session.commit()

    except Exception:
        logging.error("Unable to commit data")
        db.session.rollback()


@data_cli.command('remove')
def remove_data():
    for cell_obj in db.session.query(TimeTableCell).all():
        db.session.delete(cell_obj)

    for column_obj in db.session.query(TimeTableColumn).all():
        db.session.delete(column_obj)

    for teacher_obj in db.session.query(Teacher).all():
        teacher_obj.goals.clear()
        db.session.delete(teacher_obj)

    # noinspection PyBroadException
    try:
        db.session.commit()
        
    except Exception:
        logging.error("Unable to commit data")
        db.session.rollback()


if __name__ == '__main__':
    cli()
