from app import db
from app.utils import grade_to_quality_points


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    gpa = db.Column(db.Float, default=0.0)
    
    def calculate_gpa(self):
        total_credit_hours = 0
        total_quality_points = 0

        for registration in self.registrations:
            course = registration.course
            grade = registration.grade

            if grade:
                credit_hours = course.credit_hours
                total_credit_hours += credit_hours

                quality_points = grade_to_quality_points(grade) * credit_hours
                total_quality_points += quality_points

        if total_credit_hours > 0:
            gpa = total_quality_points / total_credit_hours
            self.gpa = round(gpa, 2)


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher = db.relationship('User', backref=db.backref('courses_taught', lazy=True))
    students = db.relationship('User', secondary='enrollments', backref='courses_enrolled')

    def __repr__(self):
        return f'<Course {self.name}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    grade = db.Column(db.Integer)

    def __repr__(self):
        return f'<Enrollment user_id={self.user_id} course_id={self.course_id}>'
