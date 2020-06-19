import enum
from datetime import date, timedelta
from collections import namedtuple

from .data import goals, teachers  # noqa

Weekday = namedtuple('Weekday', ['code', 'title'])

weekdays = (
    Weekday(code="mon", title="Понедельник"),
    Weekday(code="tue", title="Вторник"),
    Weekday(code="wed", title="Среда"),
    Weekday(code="thu", title="Четверг"),
    Weekday(code="fri", title="Пятница"),
    Weekday(code="sat", title="Суббота"),
    Weekday(code="sun", title="Воскресение"),
)


class Possibility(enum.Enum):
    PO1_2 = "1-2 часа в неделю"
    PO3_5 = "3-5 часов в неделю"
    PO5_7 = "5-7 часов в неделю"
    PO7_10 = "7-10 часов в неделю"


def get_current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return tuple(monday + timedelta(days=i) for i in range(7))
