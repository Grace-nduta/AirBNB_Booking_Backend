from server.models import Booking, db
from flask import Blueprint, request, jsonify

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/users/<int:user_id>/bookings', methods=['GET'])
def get_user_bookings(user_id):
    bookings =Booking.query.filter_by(user_id=user_id).all()
    result = []
    for booking in bookings:
        result.append({
            "id": booking.id,
            "listing_id": booking.listing_id,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "status": booking.booking_status,
            "total_price": booking.total_price,
            "created_at": booking.created_at
        })
    return jsonify(result), 200
      
@booking_bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        return jsonify({
            "id": booking.id,
            "guest": booking.guest.username,
            "listing": booking.listing.title,
            "checkin": booking.check_in,
            "checkout": booking.check_out,
            "status": booking.booking_status,
        })
    return jsonify({"error": "Booking not found"}), 404

@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json()
    new_booking = Booking(
        user_id=data['user_id'],
        listing_id=data['listing_id'],
        check_in=data['check_in'],
        check_out=data['check_out'],
        booking_status=data.get('booking_status', 'pending'),
        total_price=data['total_price']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"success": "Booking created successfully!"}), 201


@booking_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"success": "Booking cancelled successfully!"}), 200
