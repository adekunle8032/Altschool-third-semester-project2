from flask import Blueprint, jsonify, request, g
from app.db import get_db

bp = Blueprint("course_students", __name__, url_prefix="/api/course_students")

@bp.route("", methods=["GET"])
def get_course_students():
    db = get_db()
    course_students = db.execute("SELECT * FROM course_students").fetchall()
    return jsonify([dict(cs) for cs in course_students])

@bp.route("", methods=["POST"])
def create_course_student():
    db = get_db()
    data = request.get_json()
    course_id = data.get("course_id")
    student_id = data.get("student_id")
    if course_id is None:
        return jsonify({"error": "Course ID is required"}), 400
    if student_id is None:
        return jsonify({"error": "Student ID is required"}), 400
    db.execute("INSERT INTO course_students (course_id, student_id) VALUES (?, ?)", (course_id, student_id))
    db.commit()
    return jsonify({"message": "Course student relationship created successfully"})

@bp.route("/<int:course_id>/<int:student_id>", methods=["DELETE"])
def delete_course_student(course_id, student_id):
    db = get_db()
    db.execute("DELETE FROM course_students WHERE course_id = ? AND student_id = ?", (course_id, student_id))
    db.commit()
    return jsonify({"message": "Course student relationship deleted successfully"})
