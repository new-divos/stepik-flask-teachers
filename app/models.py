from . import db


teachers_goals_association = db.Table(
    'teachers_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')),

    db.PrimaryKeyConstraint(
        'teacher_id', 'goal_id',
        name='teachers_goals_association_pk'
    )
)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(150), nullable=False)
    about = db.Column('about', db.Text, nullable=True)
    rating = db.Column('rating', db.Float, nullable=False)
    picture = db.Column('picture', db.String, nullable=True)
    price = db.Column('price', db.Float, nullable=False)

    goals = db.relationship(
        'Goal',
        secondary=teachers_goals_association,
        back_populates='teachers',
        cascade='all,delete'
    )

    db.CheckConstraint(
        'rating BETWEEN 0.0 AND 5.0',
        name='rating_in_range'
    )
    db.CheckConstraint('price > 0', name='price_gt_0')


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('code', db.String(15), unique=True)
    title = db.Column('title', db.String(70), nullable=False)

    teachers = db.relationship(
        'Teacher',
        secondary=teachers_goals_association,
        back_populates='goals',
        cascade='all,delete'
    )
