from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    RadioField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, Regexp

from data import Possibility


PHONE_NUMBER_REGEXP = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}'\
                      r'[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'


class BookingForm(FlaskForm):
    client_weekday = HiddenField(id='clientWeekday')
    client_time = HiddenField(id='clientTime')
    client_teacher = HiddenField(id='clientTeacher')

    client_name = StringField(
        "Вас зовут",
        id='clientName',
        validators=[
            DataRequired("Должно быть задано имя клиента"),
            Length(
                max=70,
                message="Имя не может превышать 70 символов"
            )
        ]
    )
    client_phone = StringField(
        "Ваш телефон",
        id='clientPhone',
        validators=[
            DataRequired("Должен быть задан номер телефона клиента"),
            Length(
                max=20,
                message="Номер телефона не может превышать 20 символов"
            ),
            Regexp(
                PHONE_NUMBER_REGEXP,
                message="Номер телефона должен соответствовать шаблону"
            )
        ]
    )

    submit = SubmitField("Записаться на пробный урок")


class RequestForm(FlaskForm):
    client_goal = RadioField(
        "Какая цель занятий?",
        id='clientGoal',
        validators=[DataRequired("Требуется выбрать цель занятия")]
    )
    client_possibility = RadioField(
        "Сколько времени есть?",
        id='clientPossibility',
        validators=[
            DataRequired("Требуется выбрать сколько времени можете уделить")
        ]
    )

    client_name = StringField(
        "Вас зовут",
        id='clientName',
        validators=[
            DataRequired("Должно быть задано имя клиента"),
            Length(
                max=70,
                message="Имя не может превышать 70 символов"
            )
        ]
    )
    client_phone = StringField(
        "Ваш телефон",
        id='clientPhone',
        validators=[
            DataRequired("Должен быть задан номер телефона клиента"),
            Length(
                max=20,
                message="Номер телефона не может превышать 20 символов"
            ),
            Regexp(
                PHONE_NUMBER_REGEXP,
                message="Номер телефона должен соответствовать шаблону"
            )
        ]
    )

    submit = SubmitField("Найдите мне преподавателя")

    def __init__(self, goals, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

        self.client_goal.choices = [(goal.code, goal.title) for goal in goals]
        self.client_possibility.choices = [(possibility.name, possibility.value)
                                           for possibility in Possibility]
