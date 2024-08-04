from flask import Blueprint, request, jsonify, current_app
from modules.models import Project, User, Organization, Label, Task, TaskAssignee, TaskLabel, TaskHistory
from modules.common.db_init import db
from datetime import datetime, timedelta

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['POST'])
def create_tasks():
    user_id = request.json.get("user_id")
    if user_id is None or not isinstance(user_id, int):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404
    username = request.json.get("username")

    if username is None or not isinstance(username, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'username'"}), 404

    title = request.json.get("tasks_title")
    if title is None or not isinstance(title, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'tasks_title'"}), 404

    title_description = request.json.get("description")
    if title_description is None or not isinstance(title_description, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'description'"}), 404

    title_status = request.json.get("status")
    if title_status is None:
        title_status = 'PENDING'
    elif title_status is not None and not isinstance(title_status, str):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'status'"}), 404

    priority = request.json.get("priority", None)
    # if title_priority is not None and not isinstance(title_priority, int):
    #     return jsonify({"status": False, "message": "Invalid value for payload key: 'priority'"}), 404

    effort_hours = request.json.get("effort_hours", None)
    if effort_hours is not None and not isinstance(effort_hours, int):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'effort_hours'"}), 404

    project_id = request.json.get("project_id", None)
    if project_id is not None and not isinstance(project_id, int):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'project_id'"}), 404

    default_deadline = datetime.now() + timedelta(weeks=1)

    user_id = int(user_id)
    task_user_id = db.session.query(User).filter(User.username == username).first().id
    task = Task(
        title=title,
        description=title_description,
        status=title_status,
        priority=priority or None,
        deadline=default_deadline,
        effort_hours=effort_hours,
        project_id=project_id
    )
    db.session.add(task)
    db.session.commit()
    task_assginee = TaskAssignee(task_id=task.id, assigned_to_user_id=task_user_id)
    db.session.add(task_assginee)
    db.session.commit()

    return jsonify({"success": True}), 202


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    task_id = int(task_id)
    task_assignee = TaskAssignee(task_id=task_id, assigned_to_user_id=user_id)
    db.session.delete(task_assignee)

    tasklabels = db.session.query(TaskLabel).filter(TaskLabel.task_id==task_id)
    for labels in tasklabels:
        task_labels = TaskLabel(task_id=labels.task_id, label_id=labels.id)
        db.session.delete(task_labels)

    labels = db.session.query(Label).join(
        TaskLabel,
        TaskLabel.label_id==Label.id
    ).filter(
        TaskLabel.task_id==task_id
    )
    for label in labels:
        lab = Label(label_name=label.label_name, description=label.description)
        db.session.delete(lab)

    taskhistory = db.session.query(TaskHistory).filter(TaskHistory.task_id == task_id)
    for history in taskhistory:
        task_labels = TaskLabel(task_id=history.task_id,
                                user_id=history.user_id,
                                timestamp=history.timestamp,
                                field_changed=history.field_changed,
                                old_value=history.old_value)
        db.session.delete(task_labels)

   # task = Task()
    db.session.delete(Task)
    task_labels = TaskLabel(task_id=task_id)
    db.session.delete(task_labels)
    task = db.session.query(Task).filter(Task.id==task_id).first()
    db.session.delete(task)
    db.session.commit()

    return jsonify({"success": True, "message": " Task Deleted successfully"}), 202


@task_bp.route('/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    user_id = request.json.get("user_id")
    if not user_id or not isinstance(user_id, int):
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    func = db.session.query(TaskAssignee).filter()
    task_id = int(task_id)
    taskassignee = TaskAssignee(task_id=task_id, assigned_to_user_id=user_id)
    db.session.add(taskassignee)
    db.session.commit()
    task_assign_data = {
        "task_id": task_id,
        "assigned_to_user_id": user_id
    }
    return jsonify({"success": True,"data": task_assign_data, "message": " Task Deleted successfully"}), 202


@task_bp.route('/tasks', methods=['GET'])
def view_task_assigned_to_user():
    user_id = request.args.get("user_id")
    if not user_id or not user_id.isnumeric():
        return jsonify({"status": False, "message": "Invalid value for payload key: 'user_id'"}), 404

    task_data = db.session.query(Task, User).join(
        TaskAssignee,
        Task.id == TaskAssignee.task_id,
    ).filter(
        User.id == TaskAssignee.assigned_to_user_id,
        TaskAssignee.assigned_to_user_id == user_id
    )
    all_tasks = []
    for task in task_data:
        all_tasks.append({
            "task_id": task[0].id,
            "task_title": task[0].title,
            "task_status": task[0].status,
            "task_deadline": task[0].deadline,
            "task_assigned_user": task[1].username
        })
    return jsonify({"success": True, "data": all_tasks}), 200

""" 
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_details(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    # Update task details
    status = request.json.get("status")
    if status is not None and isinstance(status, str):
        task.status = status

    title = request.json.get("title")
    if title is not None and isinstance(title, str):
        task.title = title

    description = request.json.get("description")
    if description is not None and isinstance(description, str):
        task.description = description

    deadline = request.json.get("deadline")
    if deadline is not None:
        task.deadline = deadline

    priority = request.json.get("priority")
    if priority is not None and isinstance(priority, int):
        task.priority = priority

    effort_hours = request.json.get("effort_hours")
    if effort_hours is not None and isinstance(effort_hours, int):
        task.effort_hours = effort_hours

    # Commit all updates to the database
    db.session.commit()

    return jsonify({"message": "Task updated successfully"}), 200
"""


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_details(task_id):
    
    status = request.json.get("status")
    if status is not None and isinstance(status, str):
        task = db.session.query(Task).filter(
            Task.id == task_id
        ).update(
            {Task.status: status}
        )

    title = request.json.get("title")
    if title is not None and isinstance(title, str):
        task = db.session.query(Task).filter(
            Task.id == task_id
        ).update(
            {Task.title: title}
        )
        
    description = request.json.get("description")
    if description is not None and isinstance(title, str):
        task = db.session.query(Task).filter(
            Task.id == task_id
        ).update(
            {Task.description: description}
        )
        
    deadline = request.json.get("deadline")
    if deadline is not None and isinstance(title, str):
        task = db.session.query(Task).filter(
            Task.id == task_id
        ).update(
            {Task.deadline: deadline}
        )
    priority = request.json.get("priority")
    if priority is not None and isinstance(priority, str):
        task = db.session.query(Task).filter(
            Task.id == task_id
        ).update(
            {Task.priority: priority}
        )

        
    effort_hours = request.json.get("effort_hours")
    if effort_hours is not None and isinstance(priority, str):
        task = db.session.query(Task).filter(
            Task.id == task_id
        ).update(
            {Task.efforthours: effort_hours}
        )
    db.session.commit()
    return jsonify({"message": "Task updated successfully"}), 200



d