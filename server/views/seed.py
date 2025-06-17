users = [
    {"username":"Jayden Kamau", "email":"jayden@gmail.com", "password":"jay123", "role":"host"},
    {"username":"Margaret Wambui", "email":"margaret@gmail.com", "password":"magimagi", "role":"guest"},
    {"username": "Jason Kahare", "email": "jay@gmail.com", "password": "jayjay124", "role": "guest"},
    {"username": "George Kamau", "email": "kamau3@gmail.com", "password": "kamaubeme123", "role": "guest"},
    {"username": "William Muiruri", "email":"muiruri@gmail.com", "password":"muiruri123", "role":"Admin"},
]

listings = [
    {"id":1 , "user_id": 1, "title": "Cozy Cottage", "description": "A cozy cottage in the countryside.", "price_per_night": 100.0, "amenities": "WiFi, Kitchen, Parking", "image_url": ""},
    {"id":2 , "user_id": 1, "title": "Modern Apartment", "description": "A modern apartment in the city center.", "price_per_night": 150.0, "amenities": "WiFi, Air Conditioning, Pool", "image_url": ""},
    {"id":3 , "user_id": 2, "title": "Beach House", "description": "A beautiful beach house with ocean views.", "price_per_night": 200.0, "amenities": "WiFi, Beach Access, Pool", "image_url": ""},
    {"id":4 , "user_id": 2, "title": "Mountain Cabin", "description": "A rustic cabin in the mountains.", "price_per_night": 120.0, "amenities": "WiFi, Fireplace, Hiking Trails", "image_url": ""},
    {"id":5 , "user_id": 3, "title": "Luxury Villa", "description": "A luxury villa with a private pool.", "price_per_night": 300.0, "amenities": "WiFi, Pool, Spa", "image_url": ""},
]

bookings = [
    {"id":1, "user_id": 2, "listing_id": 1, "booking_status": "completed", "total_price": 400.0},
    {"id":2, "user_id": 3, "listing_id": 2,  "booking_status": "pending", "total_price": 750.0},
    {"id":3, "user_id": 4, "listing_id": 3,  "booking_status": "completed", "total_price": 1400.0},
    {"id":4, "user_id": 5, "listing_id": 4,  "booking_status": "pending", "total_price": 240.0},
    {"id":5, "user_id": 1, "listing_id": 5,  "booking_status": "completed", "total_price": 900.0},
]

favorites = [
    {"id":1, "user_id": 2, "listing_id": 1, "note": "Looking forward to booking this next month!"},
    {"id":2, "user_id": 3, "listing_id": 2, "note": "This place looks amazing!"},
    {"id":3, "user_id": 4, "listing_id": 3, "note": "Can't wait to stay here!"},
    {"id":4, "user_id": 5, "listing_id": 4, "note": "This is my dream vacation spot!"},
    {"id":5, "user_id": 1, "listing_id": 5, "note": "Perfect for a weekend getaway!"},
]