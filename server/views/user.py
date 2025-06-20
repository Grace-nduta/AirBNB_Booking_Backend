from flask import Blueprint, request, jsonify
from models import db, User, Booking, Favorites, Review
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if current_user.role == 'guest':
        if current_user_id != user_id or user.role !='guest':
            return jsonify({'error': 'You are not authorized to view this user'}), 403
        
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role})

    

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'guest')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
    if existing_email:
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role=role
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": "New user created successfully!"}), 201


@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)
    if not current_user or current_user.role != 'guest':
        return jsonify({"error": "You are not authorized to update this account!"}), 403

    data = request.json
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    if 'role' in data:
        if current_user.role == 'admin':
            user.role = data['role']
        else:
            return jsonify({"error": "You are not authorized to change the role!"}), 403

    db.session.commit()
    return jsonify({"success": "User updated successfully!"})


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)
    if not current_user or current_user.role != 'guest':
        return jsonify({"error": "You are not authorized to delete this account!"}), 403
    Booking.query.filter_by(user_id=user.id).delete()
    Favorites.query.filter_by(user_id=user.id).delete()
    Review.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "User deleted successfully!"})
