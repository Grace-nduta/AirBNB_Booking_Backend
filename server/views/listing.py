from flask import Blueprint, request, jsonify
from server.models import Listing, db

listing_bp = Blueprint('listing', __name__)

@listing_bp.route('/listings', methods=['GET'])
def get_all_listings():
    listings = Listing.query.all()
    result = []
    for listing in listings:
        result.append({
            "id": listing.id,
            "title": listing.title,
            "location": listing.location,
            "description": listing.description,
            "price_per_night": listing.price_per_night,
            "amenities": listing.amenities,
            "image_url": listing.image_url,
            "host_id": listing.user_id,
            "created_at": listing.created_at
        })
    return jsonify (result), 200

@listing_bp.route('/listings/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if listing:
        return jsonify({
            "id": listing.id,
            "title": listing.title,
            "description": listing.description,
            "price_per_night": listing.price_per_night,
            "amenities": listing.amenities,
            "image_url": listing.image_url,
            "host_id": listing.user_id,
            "created_at": listing.created_at
        })
    return jsonify({"error": "Listing not found"}), 404

@listing_bp.route('/listings', methods=['POST'])
def create_listing():
    data = request.json
    new_listing = Listing(
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        price_per_night=data['price_per_night'],
        amenities=data.get('amenities', ''),
        image_url=data.get('image_url', '')
    )
    db.session.add(new_listing)
    db.session.commit()
    return jsonify({"success": "Listing created successfully!"}), 201

