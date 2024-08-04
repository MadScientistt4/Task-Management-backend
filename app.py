import os
from flask import Flask, make_response, jsonify, request
from modules.common.db_init import db

def load_config(app):
    global_config_path = os.path.join(app.root_path, "config.py")
    app.config.from_pyfile(global_config_path)

def register_blueprints(app):
    from modules.projects.views import project_bp
    app.register_blueprint(project_bp)
    from modules.tasks.views import task_bp
    app.register_blueprint(task_bp)
    from modules.login.views import login_bp
    app.register_blueprint(login_bp)
    from modules.signup.views import signup_bp
    app.register_blueprint(signup_bp)

def create_app():
    app = Flask(__name__)
    load_config(app)
    # Explicitly allow only the React app's origin and specify methods
    #CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": "GET,POST,PUT,DELETE,OPTIONS"}})
    db.init_app(app=app)

    from modules.models import (
        Organization, Project, Permission, Team, Task, TaskAssignee, TaskHistory, TaskLabel,
        ProjectAssignee, Comment, Label
    )
    with app.app_context():
        db.create_all()
    register_blueprints(app)

    print("#" * 50, f"{' ' * 10} * STARTING APP", "#" * 50, sep='\n')

    return app

app = create_app()
"""
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Add a route to handle OPTIONS requests
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
    
    
"""
if __name__ == "__main__":
    app.run(port=5000, debug=True)
