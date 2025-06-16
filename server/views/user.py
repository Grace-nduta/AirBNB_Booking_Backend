from flask import Blueprint, request, jsonify
from server.models import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role} for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role})

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'guest')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success":"New user created successfully!"}), 201

@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'role' in data:
        user.role = data['role']

    db.session.commit()
    return jsonify({"success": "User updated successfully!"})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Ooops! User not found."}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "User deleted successfully!"})


