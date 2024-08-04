from flask import Blueprint, request, jsonify
from modules.models import Project, User, Organization, Task
from modules.common.db_init import db

signup_bp = Blueprint('signup', __name__)


@signup_bp.route('/signup', methods=['POST'])
def signup():
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    username = request.json.get("username")
    if username is None or not isinstance(username, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'project_name'"}), 404

    email = request.json.get("email")
    if email is None or not isinstance(email, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'email'"}), 404

    org_name = request.json.get("organization_name")
    if org_name is None or not isinstance(org_name, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'organization'"}), 404

    password = request.json.get("password")
    if password is None or not isinstance(password, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'password'"}), 404

    confirm_password = request.json.get("confirm_password")
    if confirm_password is None or not isinstance(confirm_password, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'conf password'"}), 404

    user_name = db.session.query(User).filter(User.username == username).first()
    if user_name is not None:
        return jsonify({"message": f"User with username: {username} already exists "})

    emails = db.session.query(User).filter(User.email == email).first()
    if emails is not None:
        return jsonify({"message": f"User with username: {emails} already exists "})

    org = db.session.query(Organization).filter(Organization.name == org_name).first()
    if org is None:
        return jsonify({"message": f"Organization with name: {org_name} does not exists "})

    if password != confirm_password:
        return jsonify({"message": f"passwords does not match "})

    user = User(id=user_id, username=username, email=email, password_hash=password, organization_id=org.id)
    db.session.add(user)
    db.session.commit()
    user_data = {
        'username': username,
        'email': email,
        'organization_name': org_name,
        'password': password
    }
    return jsonify({"success": True, "data": user_data, "message": "Successfully signed up"}), 202
