from flask import Blueprint, jsonify, request
from models import Booking, db

booking_bp = Blueprint('booking', __name__)

# ========== Get all bookings for a user =========
@booking_bp.route('/users/<int:user_id>/bookings', methods=['GET'])
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
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

# Look at it later
@booking_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    user_id = data['user_id']
    listing_id = data['listing_id']
    check_in = data['check_in']
    check_out = data['check_out']
    # total_price = data['total_price']
    # booking_status = data.get('booking_status', 'pending')

    # Check for overlapping bookings
    overlapping = Booking.query.filter(
        Booking.listing_id == listing_id,
        Booking.check_out > check_in,
        Booking.check_in < check_out
    ).first()
    if overlapping:
        return jsonify({'error': 'Listing is not available for the selected dates.'}), 400

    new_booking = Booking(
        user_id=user_id,
        listing_id=listing_id,
        check_in=check_in,
        check_out=check_out,
        # booking_status=booking_status,
        # total_price=total_price
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'success': 'Booking created successfully!'}), 201


@booking_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"success": "Booking cancelled successfully!"}), 200

# Check availability for a listing
@booking_bp.route('/listings/<int:listing_id>/availability', methods=['POST'])
def check_availability(listing_id):
    data = request.get_json()
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    if not check_in or not check_out:
        return jsonify({'error': 'check_in and check_out dates required'}), 400

    # Query for overlapping bookings
    overlapping = Booking.query.filter(
        Booking.listing_id == listing_id,
        Booking.check_out > check_in,
        Booking.check_in < check_out
    ).first()

    if overlapping:
        return jsonify({'available': False, 'error': 'Listing is not available for the selected dates.'}), 200
    else:
        return jsonify({'available': True, 'success': 'Listing is available for the selected dates.'}), 200
