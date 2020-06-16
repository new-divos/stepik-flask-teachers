from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from sqlalchemy.sql.expression import func

from . import main
from .forms import BookingForm, RequestForm
from .. import db
from ..models import (
    Goal,
    Teacher,
)


@main.route('/')
def index():
    goals = db.session.query(Goal).order_by(Goal.title)
    teachers = db.session.query(Teacher).order_by(func.random()).limit(6)

    return render_template('index.html', goals=goals, teachers=teachers)


@main.route('/goals/<code>/')
def render_goal(code: str):
    goal = db.session.query(Goal).filter(Goal.code == code).first()
    if goal is None:
        abort(404)

    return render_template('goal.html', goal=goal, teachers=goal.teachers)


@main.route('/profiles/<int:id>/')
def render_profile(id: int):
    # storage = Storage()
    # teacher = next((t for t in storage.teachers if t['id'] == id), None)
    # if teacher is None:
    #     abort(404)
    #
    # goals = [g['title'] for g in storage.goals if g['code'] in teacher['goals']]
    #
    # time_table = OrderedDict()
    # for code, name in storage.weekdays.items():
    #     hour_lst = [('0' + hour if len(hour) < 5 else hour, int(hour.split(':')[0]))
    #                 for hour, free in teacher['free'].get(code, dict()).items() if free]
    #     hour_lst.sort(key=lambda item: item[1])
    #
    #     time_table[(code, name)] = OrderedDict(hour_lst)
    #
    # return render_template('profile.html',
    #                        teacher=teacher,
    #                        goals=goals,
    #                        time_table=time_table)
    pass


@main.route('/booking/<int:id>/<code>/<int:hour>/')
def render_booking(id, code, hour):
    # storage = Storage()
    # teacher = next((t for t in storage.teachers if t['id'] == id), None)
    # if teacher is None:
    #     abort(404)
    #
    # if code not in storage.weekdays:
    #     abort(404)
    #
    # time = f'{hour}:00'
    # if time not in teacher['free'].get(code, dict()) or \
    #         not teacher['free'][code].get(time, False):
    #     return redirect(url_for('main.render_profile', id=id))
    #
    # form = BookingForm()
    # return render_template('booking.html',
    #                        teacher=teacher,
    #                        weekday=(code, storage.weekdays[code]),
    #                        time=time,
    #                        form=form)
    pass


@main.route('/booking_done/', methods=('POST', ))
def render_booking_done():
    # storage = Storage()
    # form = BookingForm()
    #
    # id = int(form.client_teacher.data)
    # code = form.client_weekday.data
    # time = form.client_time.data
    #
    # if form.validate_on_submit():
    #     teacher = next((t for t in storage.teachers if t['id'] == id), None)
    #     if teacher is None:
    #         abort(404)
    #
    #     weekday = storage.weekdays.get(code)
    #     if weekday is None:
    #         abort(404)
    #
    #     if time not in teacher['free'].get(code, dict()) or \
    #             not teacher['free'][code].get(time, False):
    #         return redirect(url_for('main.render_profile', id=id))
    #
    #     name = form.client_name.data.strip()
    #     phone = form.client_phone.data.strip()
    #
    #     teacher['free'][code][time] = False
    #     storage.update()
    #
    #     return render_template('booking_done.html',
    #                            teacher=teacher,
    #                            weekday=weekday,
    #                            time=time,
    #                            name=name,
    #                            phone=phone)
    #
    # else:
    #     for field_errors in form.errors.values():
    #         for error in field_errors:
    #             flash(error, 'error')
    #
    #     hour = int(time.split(':')[0])
    #     return redirect(url_for('main.render_booking', id=id, code=code, hour=hour))
    pass


@main.route('/request/')
def render_request():
    # storage = Storage()
    # form = RequestForm(storage)
    #
    # return render_template('request.html', form=form)
    pass


@main.route('/request_done/', methods=('POST', ))
def render_request_done():
    # storage = Storage()
    # form = RequestForm(storage)
    #
    # if form.validate_on_submit():
    #     code = form.client_goal.data
    #     goal = next((g['title'] for g in storage.goals if g['code'] == code), None)
    #     if goal is None:
    #         abort(404)
    #
    #     code = form.client_opportunity.data
    #     opportunity = next((o[1] for o in storage.opportunities if o[0] == code), None)
    #     if opportunity is None:
    #         abort(404)
    #
    #     name = form.client_name.data.strip()
    #     phone = form.client_phone.data.strip()
    #
    #     return render_template('request_done.html',
    #                            goal=goal,
    #                            opportunity=opportunity,
    #                            name=name,
    #                            phone=phone)
    #
    # else:
    #     for field_errors in form.errors.values():
    #         for error in field_errors:
    #             flash(error, 'error')
    #
    #     return redirect(url_for('main.render_request'))
    pass


@main.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(current_app.config['APP_STATIC_DIR'], filename)
