from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from app.models import Student, Course, Enrollment, Grade

ma = Marshmallow()


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        include_fk = True


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        include_fk = True


class EnrollmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Enrollment
        include_fk = True


class GradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Grade
        include_fk = True


def validate_student_id(student_id):
    if not Student.query.get(student_id):
        raise ValidationError(f"Invalid student ID: {student_id}")


def validate_course_id(course_id):
    if not Course.query.get(course_id):
        raise ValidationError(f"Invalid course ID: {course_id}")


def validate_student_enrolled_in_course(student_id, course_id):
    if not Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        raise ValidationError(f"Student with ID {student_id} is not enrolled in course with ID {course_id}")


def validate_grade_in_range(grade):
    if not (0 <= grade <= 100):
        raise ValidationError("Grade must be between 0 and 100")
