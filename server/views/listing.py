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
            "location": listing.location,
            "image_url": listing.image_url,
            
        })
    return jsonify({"error": "Listing not found"}), 404

@listing_bp.route('/listings', methods=['GET'])
def get_listings():
    title = request.args.get('title')
    location = request.args.get('location')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Listing.query
    if title:
        query = query.filter(Listing.title.like(f'%{title}%'))
    if location:
        query = query.filter(Listing.location.like(f'%{location}%'))
    if min_price:
        query = query.filter(Listing.price_per_night >= min_price)

    if max_price:
        query = query.filter(Listing.price_per_night <= max_price)

    listings = query.all()
    return jsonify([listing.to_dict() for listing in listings])




