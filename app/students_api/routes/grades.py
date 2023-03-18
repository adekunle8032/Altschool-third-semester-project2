from flask import Blueprint, jsonify, request, g
from app.db import get_db

bp = Blueprint("grades", __name__, url_prefix="/api/grades")

@bp.route("", methods=["GET"])
def get_grades():
    db = get_db()
    grades = db.execute("SELECT * FROM grades").fetchall()
    return jsonify([dict(grade) for grade in grades])

@bp.route("", methods=["POST"])
def create_grade():
    db = get_db()
    data = request.get_json()
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    grade = data.get("grade")
    if student_id is None:
        return jsonify({"error": "Student ID is required"}), 400
    if course_id is None:
        return jsonify({"error": "Course ID is required"}), 400
    if grade is None:
        return jsonify({"error": "Grade is required"}), 400
    db.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
    db.commit()
    return jsonify({"message": "Grade created successfully"})

@bp.route("/<int:id>", methods=["GET"])
def get_grade(id):
    db = get_db()
    grade = db.execute("SELECT * FROM grades WHERE id = ?", (id,)).fetchone()
    if grade is None:
        return jsonify({"error": "Grade not found"}), 404
    return jsonify(dict(grade))

@bp.route("/<int:id>", methods=["PUT"])
def update_grade(id):
    db = get_db()
    data = request.get_json()
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    grade = data.get("grade")
    if student_id is None:
        return jsonify({"error": "Student ID is required"}), 400
    if course_id is None:
        return jsonify({"error": "Course ID is required"}), 400
    if grade is None:
                return jsonify({"error": "Grade is required"}), 400
    db.execute("UPDATE grades SET student_id = ?, course_id = ?, grade = ? WHERE id = ?", (student_id, course_id, grade, id))
    db.commit()
    return jsonify({"message": "Grade updated successfully"})

@bp.route("/<int:id>", methods=["DELETE"])
def delete_grade(id):
    db = get_db()
    db.execute("DELETE FROM grades WHERE id = ?", (id,))
    db.commit()
    return jsonify({"message": "Grade deleted successfully"})

    