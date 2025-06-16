from flask import Blueprint, jsonify, request
from server.models import Admin, db , User, Listing , Booking
from flask_jwt_extended import jwt_required, get_jwt_identity
admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@admin_blueprint.route('/listings', methods=['GET'])
@jwt_required()
def get_all_listings():
    current_user = get_jwt_identity()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    listings = Listing.query.all()
    return jsonify([listing.to_dict() for listing in listings]), 200

@admin_blueprint.route('users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    current_user = get_jwt_identity()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "User deleted successfully"}), 200

@admin_blueprint.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    current_user = get_jwt_identity()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"error": "Listing not found"}), 404
    db.session.delete(listing)
    db.session.commit()
    return jsonify({"success": "Listing deleted successfully"}), 200
    
@admin_blueprint.route('/analytics', methods=['GET'])
def get_analytics():
    @jwt_required()
    current_user = get_jwt_identity()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Booking.total_price)).scalar() or 0

    popular_locations = db.session.query(
        Listing.location,
        db.func.count(Booking.id).label('booking_count')
    ).join(Booking, Booking.listing_id == Listing.id) .group_by(Listing.location)  .order_by(db.desc('booking_count')).all()

    return jsonify({
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'popular_locations' : [{'location' : loc, 'bookings' : count} for loc, count in popular_locations]
    })
    
# promote or demote a user from guest to host or vice versa
@admin_blueprint.route('/users/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
def change_user_role(user_id):
    current_user = get_jwt_identity()
    if current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    new_role = data.get('role')
    if new_role not in ['guest', 'host', 'admin']:
        return jsonify({"error": "Invalid role"}), 400
    
    user.role = new_role
    db.session.commit()
    return jsonify({"success": f"User role changed to {new_role}"}), 200