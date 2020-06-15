#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from flask.cli import FlaskGroup, AppGroup
from flask_migrate import Migrate

from app import create_app, db
from app.models import (
    Goal,
    Teacher,
)
from config import config


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
        Goal=Goal,
        Teacher=Teacher,
    )


data_cli = AppGroup('data')
app.cli.add_command(data_cli)


@data_cli.command('add')
def append_data():
    from data import teachers

    goals = dict()
    for goal in db.session.query(Goal).all():
        goals[goal.code] = goal

    for teacher in teachers:
        id = teacher.get('id', -1)
        if id < 0:
            logging.warning(f"Illegal teacher identifier {id}")
            continue

        teacher_obj = db.session.query(Teacher).filter(
            Teacher.id == id
        ).first()
        if teacher_obj is not None:
            continue

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

    db.session.commit()


@data_cli.command('remove')
def remove_data():
    print("Remove data")


if __name__ == '__main__':
    cli()
