from collections import namedtuple

from .data import goals, teachers  # noqa

Weekday = namedtuple('Weekday', ['slug', 'title'])

weekdays = (
    Weekday(slug="mon", title="Понедельник"),
    Weekday(slug="tue", title="Вторник"),
    Weekday(slug="wed", title="Среда"),
    Weekday(slug="thu", title="Четверг"),
    Weekday(slug="fri", title="Пятница"),
    Weekday(slug="sat", title="Суббота"),
    Weekday(slug="sun", title="Воскресение"),
)
