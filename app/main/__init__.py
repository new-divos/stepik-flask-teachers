from flask import Blueprint


main = Blueprint('main', __name__)


@main.app_context_processor
def inject_weekdays():
    from data import weekdays
    return dict(weekdays=weekdays)


from . import errors, filters, views  # noqa
