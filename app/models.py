from . import db


teachers_goals_association = db.Table(
    'teachers_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')),

    db.PrimaryKeyConstraint(
        'teacher_id',
        'goal_id',
        name='teachers_goals_association_pk'
    )
)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(150), nullable=False)
    about = db.Column('about', db.Text, nullable=True)
    rating = db.Column(
        'rating',
        db.Float,
        db.CheckConstraint('rating BETWEEN 0.0 AND 5.0')
    )
    picture = db.Column('picture', db.String, nullable=True)
    price = db.Column(
        'price',
        db.Float,
        db.CheckConstraint('price >= 0.0')
    )

    goals = db.relationship(
        'Goal',
        secondary=teachers_goals_association,
        back_populates='teachers'
    )
    time_table = db.relationship(
        'TimeTableColumn',
        back_populates='teacher',
        cascade='all,delete',
        lazy='dynamic'
    )


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('code', db.String(15), unique=True)
    title = db.Column('title', db.String(70), nullable=False)

    teachers = db.relationship(
        'Teacher',
        secondary=teachers_goals_association,
        back_populates='goals'
    )


class TimeTableRow(db.Model):
    __tablename__ = 'time_table_rows'

    id = db.Column('id', db.Integer, primary_key=True)
    time = db.Column('time', db.Time, unique=True)
    slug = db.Column('slug', db.String(5), unique=True)

    cells = db.relationship(
        'TimeTableCell',
        back_populates='row',
        cascade='all,delete',
        lazy='dynamic'
    )


class TimeTableColumn(db.Model):
    __tablename__ = 'time_table_columns'

    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column('date', db.Date, nullable=False)
    teacher_id = db.Column(
        'teacher_id',
        db.Integer,
        db.ForeignKey('teachers.id')
    )

    teacher = db.relationship(
        'Teacher',
        uselist=False,
        back_populates='time_table',
        cascade='all,delete'
    )
    cells = db.relationship(
        'TimeTableCell',
        back_populates='column',
        cascade='all,delete',
        lazy='dynamic'
    )


class TimeTableCell(db.Model):
    __tablename__ = 'time_table_cells'

    id = db.Column('id', db.Integer, primary_key=True)
    row_id = db.Column(
        'row_id',
        db.Integer,
        db.ForeignKey('time_table_rows.id')
    )
    column_id = db.Column(
        'column_id',
        db.Integer,
        db.ForeignKey('time_table_columns.id')
    )
    is_free = db.Column(
        'is_free',
        db.Boolean,
        nullable=False,
        default=True
    )
    name = db.Column('name', db.String(70))
    phone = db.Column('phone', db.String(20))

    row = db.relationship(
        'TimeTableRow',
        uselist=False,
        back_populates='cells'
    )
    column = db.relationship(
        'TimeTableColumn',
        uselist=False,
        back_populates='cells'
    )
