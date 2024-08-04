from flask import Blueprint, request, jsonify
from modules.models import Project, User, Organization, Task, Label, TaskLabel, \
    Comment, ProjectAssignee, TaskAssignee, TaskHistory, Permission
from modules.common.db_init import db

project_bp = Blueprint('projects', __name__)
task_bp = Blueprint('tasks', __name__)


@project_bp.route('/', methods=['GET'])
def home():
    return "Welcome to our taskforge: a task management system"


@project_bp.route('/projects', methods=['GET'])
def get_all_projects():
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    user_id = int(user_id)

    all_project_results = db.session.query(Project).join(
        User,
        User.organization_id == Project.organization_id
    ).filter(
        User.id == user_id
    )

    all_projects = []
    for project in all_project_results:
        all_projects.append({
            "project_id": project.id,
            "project_name": project.project_name,
            "project_description": project.description,
        })
    return jsonify({"success": True, "data": all_projects}), 200


@project_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_all_project_tasks(project_id):
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        raise jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"})

    user_id = int(user_id)
    user = db.session.query(User).filter(User.id == user_id).first()

    all_project_tasks_results = db.session.query(
        Task, User
    ).join(
        Project,
        Project.id == Task.project_id,
    ).join(
        TaskAssignee,
        TaskAssignee.task_id == Task.id
    ).join(
        User,
        User.id == TaskAssignee.assigned_to_user_id
    ).filter(
        Project.organization_id == user.organization_id,
        Project.id == project_id
    )

    all_project_tasks = []
    for task in all_project_tasks_results:
        all_project_tasks.append({
            "task_id": task[0].id,
            "task_title": task[0].title,
            "task_status": task[0].status,
            "task_deadline": task[0].deadline,
            "task_assigned_user": task[1].username
        })
    return jsonify({"success": True, "data": all_project_tasks}), 202


@project_bp.route('/projects', methods=['POST'])
def create_project():
    user_id = request.json.get("user_id")
    if not user_id or not isinstance(user_id, int):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404
    name = request.json.get("project_name")
    if name is None or not isinstance(name, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'project_name'"}), 404
    project_description = request.json.get("description")
    if project_description is None or not isinstance(project_description, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'description'"}), 404

    user_id = int(user_id)
    user = db.session.query(User).filter(User.id == user_id).first()
    org_id = user.organization_id

    project = Project(project_name=name, description=project_description, organization_id=org_id)
    db.session.add(project)
    db.session.commit()
    project_data = {
        'id': project.id,
        'project_name': name,
        'description': project_description

    }
    return jsonify({"success": True, "data": project_data}), 202


@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    project_id = int(project_id)
    project = db.session.query(Project).filter(Project.id == project_id).first()
    project_tasks = db.session.query(Task).filter(Project.id == project_id)

    project_assign = db.session.query(ProjectAssignee).filter(Project.id == project_id)

    project_tasks_assignee = db.session.query(TaskAssignee).join(
        Task,
        TaskAssignee.task_id == Task.id
    ).filter(Task.project_id == project_id)

    task_comment = db.session.query(Comment).join(
        Task,
        Comment.task_id == Task.id
    ).filter(Task.project_id == project_id)

    task_label = db.session.query(TaskLabel).join(
        Task,
        Comment.task_id == Task.id
    ).filter(Task.project_id == project_id)

    label = db.session.query(Label).join(
        TaskLabel,
        TaskLabel.task_id == Label.id
    ).join(
        Task,
        Task.project_id == project_id)

    task_history = db.session.query(TaskHistory).join(
        Task,
        TaskHistory.task_id == Task.id
    ).filter(Task.project_id == project_id)

    permission = db.session.query(Permission).filter(Task.project_id == project_id)

    db.session.delete(project_tasks)
    db.session.delete(project_assign)
    db.session.delete(project_tasks_assignee)
    db.session.delete(task_comment)
    db.session.delete(task_label)
    db.session.delete(label)
    db.session.delete(task_history)
    db.session.delete(permission)
    db.session.delete(project)

    db.session.commit()

    return jsonify({"success": True, "message": " Task Deleted successfully"}), 202


@project_bp.route('/projects/<int:project_id>', methods=['POST'])
def add_user_to_project(project_id):
    user_id = request.json.get("user_id")
    if not user_id or not isinstance(user_id, int):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    project_members = ProjectAssignee(project_id=project_id, assigned_to_user_id=user_id)
    db.session.add(project_members)
    db.session.commit()

    return jsonify({"success": True, "message": f" User:{user_id} added to project successfully"}), 202


@project_bp.route('/projects/<int:project_id>/users', methods=['GET'])
def all_user_in_project(project_id):
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404
    all_members_results = db.session.query(User).join(
        ProjectAssignee,
        User.id == ProjectAssignee.assigned_to_user_id
    ).filter(
        ProjectAssignee.project_id==project_id
    )
    all_members = []
    for user in all_members_results:
        all_members.append({
            "user_id": user.id,
            "username": user.username
        })
    return jsonify({"success": True, "data": all_members}), 200
