from modules.common.db_init import db
from modules.common.models import BaseModel
from sqlalchemy import Enum, ForeignKey


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))



class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    # start_date = db.Column(db.Date)
    # end_date = db.Column(db.Date)
    organization_id = db.Column(db.Integer, ForeignKey('organizations.id'))




class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    organization_id = db.Column(db.Integer, ForeignKey('organizations.id'), nullable=False)



TaskStatuses = ["PENDING", "IN_PROGRESS", "DONE"]

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(Enum(*TaskStatuses))
    priority = db.Column(db.Integer)
    deadline = db.Column(db.Date)
    effort_hours = db.Column(db.Numeric(5, 2))
    # actual_time_spent = db.Column(db.Numeric(5, 2))
    project_id = db.Column(db.Integer, ForeignKey('projects.id'))



class TaskAssignee(db.Model):
    __tablename__ = 'task_assignees'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('tasks.id'))
    assigned_to_user_id = db.Column(db.Integer, ForeignKey('users.id'))



class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('tasks.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    timestamp = db.Column(db.Date)
    comment_text = db.Column(db.String(255))



class Label(db.Model):
    __tablename__ = 'labels'

    id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))



class TaskLabel(db.Model):
    __tablename__ = 'task_labels'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('tasks.id'))
    label_id = db.Column(db.Integer, ForeignKey('labels.id'))


class TaskHistory(db.Model):
    __tablename__ = 'task_history'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('tasks.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    timestamp = db.Column(db.Date)
    field_changed = db.Column(db.String(50))
    old_value = db.Column(db.String(255))
    new_value = db.Column(db.String(255))



class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    project_id = db.Column(db.Integer, ForeignKey('projects.id'))
    permission_level = db.Column(db.String(20))


# class ActivityLog(db.Model):
#     __tablename__ = 'activity_logs'
#
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, ForeignKey('users.id'))
#     activity_type = db.Column(db.String(50))
#     timestamp = db.Column(db.Date)
#     ip_address = db.Column(db.String(50))
#
#     user = db.relationship('User', back_populates='activity_logs')


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    organization_id = db.Column(db.Integer, ForeignKey('organizations.id'))


class ProjectAssignee(db.Model):
    __tablename__ = 'project_assignees'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, ForeignKey('projects.id'))
    assigned_to_user_id = db.Column(db.Integer, ForeignKey('users.id'))

