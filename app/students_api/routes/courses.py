from flask import Blueprint, jsonify, request, g
from app.db import get_db

bp = Blueprint("courses", __name__, url_prefix="/api/courses")

@bp.route("", methods=["GET"])
def get_courses():
    db = get_db()
    courses = db.execute("SELECT * FROM courses").fetchall()
    return jsonify([dict(course) for course in courses])

@bp.route("", methods=["POST"])
def create_course():
    db = get_db()
    data = request.get_json()
    name = data.get("name")
    teacher_id = data.get("teacher_id")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if teacher_id is None:
        return jsonify({"error": "Teacher ID is required"}), 400
    db.execute("INSERT INTO courses (name, teacher_id) VALUES (?, ?)", (name, teacher_id))
    db.commit()
    return jsonify({"message": "Course created successfully"})

@bp.route("/<int:id>", methods=["GET"])
def get_course(id):
    db = get_db()
    course = db.execute("SELECT * FROM courses WHERE id = ?", (id,)).fetchone()
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(dict(course))

@bp.route("/<int:id>", methods=["PUT"])
def update_course(id):
    db = get_db()
    data = request.get_json()
    name = data.get("name")
    teacher_id = data.get("teacher_id")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if teacher_id is None:
        return jsonify({"error": "Teacher ID is required"}), 400
        db.execute("UPDATE courses SET name = ?, teacher_id = ? WHERE id = ?", (name, teacher_id, id))
    db.commit()
    return jsonify({"message": "Course updated successfully"})

@bp.route("/<int:id>", methods=["DELETE"])
def delete_course(id):
    db = get_db()
    db.execute("DELETE FROM courses WHERE id = ?", (id,))
    db.commit()
    return jsonify({"message": "Course deleted successfully"})

@bp.route("/<int:id>/students", methods=["GET"])
def get_course_students(id):
    db = get_db()
    course = db.execute("SELECT * FROM courses WHERE id = ?", (id,)).fetchone()
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    students = db.execute("SELECT * FROM students WHERE id IN (SELECT student_id FROM course_students WHERE course_id = ?)", (id,)).fetchall()
    return jsonify([dict(student) for student in students])

@bp.route("/<int:id>/grades", methods=["GET"])
def get_course_grades(id):
    db = get_db()
    course = db.execute("SELECT * FROM courses WHERE id = ?", (id,)).fetchone()
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    grades = db.execute("SELECT * FROM grades WHERE course_id = ?", (id,)).fetchall()
    return jsonify([dict(grade) for grade in grades])

   
