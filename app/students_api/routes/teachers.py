from flask import Blueprint, jsonify, request, g
from app.db import get_db

bp = Blueprint("teachers", __name__, url_prefix="/api/teachers")

@bp.route("", methods=["GET"])
def get_teachers():
    db = get_db()
    teachers = db.execute("SELECT * FROM teachers").fetchall()
    return jsonify([dict(teacher) for teacher in teachers])

@bp.route("", methods=["POST"])
def create_teacher():
    db = get_db()
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if email is None:
        return jsonify({"error": "Email is required"}), 400
    db.execute("INSERT INTO teachers (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    return jsonify({"message": "Teacher created successfully"})

@bp.route("/<int:id>", methods=["GET"])
def get_teacher(id):
    db = get_db()
    teacher = db.execute("SELECT * FROM teachers WHERE id = ?", (id,)).fetchone()
    if teacher is None:
        return jsonify({"error": "Teacher not found"}), 404
    return jsonify(dict(teacher))

@bp.route("/<int:id>", methods=["PUT"])
def update_teacher(id):
    db = get_db()
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    if name is None:
        return jsonify({"error": "Name is required"}), 400
    if email is None:
        return jsonify({"error": "Email is required"}), 400
    db.execute("UPDATE teachers SET name = ?, email = ? WHERE id = ?", (name, email, id))
    db.commit()
    return jsonify({"message": "Teacher updated successfully"})

@bp.route("/<int:id>", methods=["DELETE"])
def delete_teacher(id):
    db = get_db()
    db.execute("DELETE FROM teachers WHERE id = ?", (id,))
    db.commit()
    return jsonify({"message": "Teacher deleted successfully"})
