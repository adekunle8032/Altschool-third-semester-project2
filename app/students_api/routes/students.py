from flask import Blueprint, jsonify, request, g
from app.db import get_db

bp = Blueprint("students", __name__, url_prefix="/api/students")

@bp.route("", methods=["GET"])
def get_students():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    return jsonify([dict(student) for student in students])

@bp.route("", methods=["POST"])
def create_student():
    db = get_db()
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if email is None:
        return jsonify({"error": "Email is required"}), 400
    db.execute("INSERT INTO students (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    return jsonify({"message": "Student created successfully"})

@bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    db = get_db()
    student = db.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

@bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    db = get_db()
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if email is None:
        return jsonify({"error": "Email is required"}), 400
    db.execute("UPDATE students SET name = ?, email = ? WHERE id = ?", (name, email, id))
    db.commit()
    return jsonify({"message": "Student updated successfully"})

@bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id = ?", (id,))
    db.commit()
    return jsonify({"message": "Student deleted successfully"})
