from flask import Blueprint, request, jsonify
from server.models import db, Favorites, Listing, User

favorite_bp = Blueprint('favorite_', __name__)

@favorite_bp.route('/users/<int:user_id>favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    results = []
    for favorite in favorites:
        results.append({
            "favorite_id": favorite.id,
            "listing_id": favorite.listing_id,
            "title": "",
            "description": "",
            "price_per_night": "",
            "image_url": "",
            "note": favorite.note,
            "created_at": favorite.created_at
        })
    return jsonify(results), 200
   
@favorite_bp.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    user_id = data['user_id']
    listing_id = data['listing_id']
    note = data.get('note', 'Want to book next month we gatchu you can always count on us!')
    # Check if the user and listing exist
    if not user_id or not listing_id:
        return jsonify({"error": "User_id and Listing_id required"}), 404
    # prevent duplicate favorites
    existing_favorite = Favorites.query.filter_by(user_id=user_id, listing_id=listing_id).first()
    if existing_favorite:
        return jsonify({"error": "This listing exists in your favorites"}), 400
    new_favorite = Favorites(user_id=user_id, listing_id=listing_id, note=note)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"success": "Listing added to favorites successfully!"}), 201

