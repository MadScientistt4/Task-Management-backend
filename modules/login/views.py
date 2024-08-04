from flask import Blueprint, request, jsonify, current_app, render_template
from modules.models import Project, User, Organization, Task
from modules.common.db_init import db

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET'])
def login():
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404
    email = request.json.get("email")
    if email is None or not isinstance(email, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'email'"}), 404

    password = request.json.get("password")
    if password is None or not isinstance(password, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'password'"}), 404

    user_id = int(user_id)
    user = db.session.query(User).filter(User.id == user_id).first()

    emails = db.session.query(User).filter(User.email == email).first()
    if emails is None:
        return jsonify({"message": f"User with email: {email} does not exists "})
    passwords = db.session.query(User).filter(User.email == email).filter(User.password_hash == password).first()

    if passwords is None:
        return jsonify({"message": f"Wrong password"})

    return jsonify({"success": True,"data": user_id,"message": "Successfully signed up"}), 202
