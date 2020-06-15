#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from flask.cli import FlaskGroup
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


@app.cli.command('fill_db')
def fill_db():
    pass


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Goal=Goal,
        Teacher=Teacher,
    )


if __name__ == '__main__':
    cli()
