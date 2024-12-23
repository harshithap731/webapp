from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPBasicAuth
from app.models import User, Assignment
from app import db, bcrypt

api = Blueprint('api', __name__)
auth = HTTPBasicAuth()

# Authentication verification
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None

# Routes

# Public Endpoint: Get all users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Public Endpoint: Create a new user
@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# Public Endpoint: Get all assignments
@api.route('/assignments', methods=['GET'])
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([assignment.to_dict() for assignment in assignments])

# Authenticated Endpoint: Create an assignment
@api.route('/assignments', methods=['POST'])
@auth.login_required
def create_assignment():
    data = request.get_json()
    if not (1 <= data['points'] <= 10):
        return jsonify({"error": "Points must be between 1 and 10"}), 400
    assignment = Assignment(title=data['title'], points=data['points'], user_id=auth.current_user().id)
    db.session.add(assignment)
    db.session.commit()
    return jsonify(assignment.to_dict()), 201

# Authenticated Endpoint: Update an assignment
@api.route('/assignments/<int:id>', methods=['PUT'])
@auth.login_required
def update_assignment(id):
    data = request.get_json()
    assignment = Assignment.query.get_or_404(id)
    if assignment.user_id != auth.current_user().id:
        return jsonify({"error": "Permission denied"}), 403
    assignment.title = data['title']
    assignment.points = data['points']
    db.session.commit()
    return jsonify(assignment.to_dict()), 200

# Authenticated Endpoint: Delete an assignment
@api.route('/assignments/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if assignment.user_id != auth.current_user().id:
        return jsonify({"error": "Permission denied"}), 403
    db.session.delete(assignment)
    db.session.commit()
    return '', 204

@api.route('/assignments/<int:id>', methods=['PATCH'])
def patch_not_allowed(id):
    return jsonify({"error": "PATCH method not allowed"}), 405

