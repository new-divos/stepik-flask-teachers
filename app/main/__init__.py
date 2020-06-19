from flask import Blueprint

from data import Possibility


main = Blueprint('main', __name__)


@main.app_context_processor
def _jinja2_inject_data():
    from data import weekdays
    return dict(
        Possibility=Possibility,
        weekdays=weekdays,
    )


from . import errors, filters, views  # noqa
