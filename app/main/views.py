from collections import OrderedDict

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
    ClientRequest,
    Goal,
    Teacher,
    TimeTableCell,
    TimeTableColumn,
    TimeTableRow,
)
from data import get_current_week, weekdays, Possibility


@main.route('/')
def index():
    goals = db.session.query(Goal).order_by(Goal.title)
    unordered = db.session.query(Teacher).order_by(func.random()).limit(6)

    pairs = [(t, t.rating) for t in unordered]
    pairs.sort(key=lambda item: item[1], reverse=True)
    teachers, _ = zip(*pairs)

    return render_template('index.html', goals=goals, teachers=teachers)


@main.route('/goals/<code>/')
def render_goal(code: str):
    goal = db.session.query(Goal).filter(Goal.code == code).first()
    if goal is None:
        abort(404)

    pairs = [(t, t.rating) for t in goal.teachers]
    pairs.sort(key=lambda item: item[1], reverse=True)
    teachers, _ = zip(*pairs)

    return render_template('goal.html', goal=goal, teachers=teachers)


@main.route('/profiles/<int:id>/')
def render_profile(id: int):
    teacher = db.session.query(Teacher).get_or_404(id)

    week = get_current_week()
    time_points = dict()
    for row in db.session.query(TimeTableRow):
        time_points[row.time] = (row.id, row.slug)

    time_table = OrderedDict()
    has_changed = False
    for number, time_table_date in enumerate(week):
        time_list = []
        time_table_column = db.session.query(TimeTableColumn).filter(
            (TimeTableColumn.teacher_id == id) &
            (TimeTableColumn.date == time_table_date)
        ).first()
        if time_table_column is None:
            time_table_column = TimeTableColumn(
                teacher_id=id,
                date=time_table_date
            )
            db.session.add(time_table_column)

            for time, (row_id, slug) in time_points.items():
                time_table_cell = TimeTableCell(
                    row_id=row_id,
                    column=time_table_column
                )
                db.session.add(time_table_cell)

                time_list.append((time, slug))

            has_changed = True

        else:
            for cell in time_table_column.cells.filter(TimeTableCell.is_free):
                time, slug = next(
                    ((t, s) for t, (row_id, s) in time_points.items()
                     if row_id == cell.row_id),
                    (None, None)
                )

                if time is not None and slug is not None:
                    time_list.append((time, slug))

        time_list.sort(key=lambda item: item[0])
        time_table[(number, time_table_date)] = time_list

    if has_changed:
        db.session.commit()

    return render_template(
        'profile.html',
        teacher=teacher,
        time_table=time_table
    )


@main.route('/booking/<int:id>/<code>/<slug>/')
def render_booking(id, code, slug):
    teacher = db.session.query(Teacher).get_or_404(id)

    weekday = next(
        (idx for idx, (c, _) in enumerate(weekdays) if c == code),
        None
    )
    if weekday is None:
        abort(404)

    time_table_row = db.session.query(TimeTableRow).filter(
        TimeTableRow.slug == slug
    ).first()
    if time_table_row is None:
        abort(404)

    form = BookingForm()
    return render_template(
        'booking.html',
        teacher=teacher,
        weekday=weekday,
        date=get_current_week()[weekday],
        time_table_row=time_table_row,
        form=form
    )


@main.route('/booking_done/', methods=('POST', ))
def render_booking_done():
    form = BookingForm()

    id = int(form.client_teacher.data)
    code = form.client_weekday.data
    slug = form.client_time.data

    if form.validate_on_submit():
        teacher = db.session.query(Teacher).get_or_404(id)

        weekday = next(
            (idx for idx, (c, _) in enumerate(weekdays)
             if c == form.client_weekday.data),
            None
        )
        if weekday is None:
            abort(404)

        time_table_column = db.session.query(TimeTableColumn).filter(
            (TimeTableColumn.teacher == teacher) &
            (TimeTableColumn.date == get_current_week()[weekday])
        ).first()
        if time_table_column is None:
            redirect(url_for('main.render_profile', id=id))

        time_table_row = db.session.query(TimeTableRow).filter(
            TimeTableRow.slug == slug
        ).first()
        if time_table_row is None:
            abort(404)

        name = form.client_name.data.strip()
        phone = form.client_phone.data.strip()

        time_table_cell = db.session.query(TimeTableCell).filter(
            (TimeTableCell.row == time_table_row) &
            (TimeTableCell.column == time_table_column) &
            TimeTableCell.is_free
        ).first()
        if time_table_cell is None:
            redirect(url_for('main.render_profile', id=id))
        else:
            time_table_cell.is_free = False
            time_table_cell.name = name
            time_table_cell.phone = phone

            db.session.commit()

        return render_template(
            'booking_done.html',
            weekday=weekday,
            date=time_table_column.date,
            time=time_table_row.time,
            name=name,
            phone=phone
        )

    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'error')

        return redirect(url_for(
            'main.render_booking',
            id=id,
            code=code,
            slug=slug
        ))


@main.route('/request/')
def render_request():
    form = RequestForm(db.session.query(Goal).all())
    return render_template('request.html', form=form)


@main.route('/request_done/', methods=('POST', ))
def render_request_done():
    goals = list(db.session.query(Goal).all())
    form = RequestForm(goals)

    if form.validate_on_submit():
        goal = next(
            (g for g in goals if g.code == form.client_goal.data),
            None
        )
        if goal is None:
            abort(404)

        possibility = next(
            (v for v in Possibility if v.name == form.client_possibility.data),
            None
        )
        if possibility is None:
            abort(404)

        name = form.client_name.data
        phone = form.client_phone.data

        client_request = ClientRequest(
            goal=goal,
            possibility=possibility,
            name=name,
            phone=phone
        )

        db.session.add(client_request)
        db.session.commit()

        return render_template(
            'request_done.html',
            goal=goal,
            possibility=possibility,
            name=name,
            phone=phone
        )

    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, 'error')

        return redirect(url_for('main.render_request'))


@main.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(current_app.config['APP_STATIC_DIR'], filename)
