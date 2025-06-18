from flask import jsonify, request, Blueprint
from server.models import Review, db
review_bp = Blueprint('review', __name__)

@review_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    new_review = Review(
        user_id=data['user_id'],
        listing_id=data['listing_id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"success": "Review added!"}), 201