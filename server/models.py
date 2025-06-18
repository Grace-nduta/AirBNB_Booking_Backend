# server/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import MetaData
metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
from datetime import datetime

db = SQLAlchemy()

#----User Model----
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='guest') # 'guest', 'host' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    bookings = db.relationship('Booking', backref='guest', lazy=True)
    listings = db.relationship('Listing', backref='host', lazy=True)
    favorites = db.relationship('Favorites', backref='user', lazy=True)
    
#----Booking Model---- 
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    check_in = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    check_out = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    booking_status = db.Column(db.String(20), default='pending', nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#__-Listing Model----
class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(300), nullable=True)

    # Relationships
    bookings = db.relationship('Booking', backref='listing', lazy=True)
    favorited_by = db.relationship('Favorites', backref='listing', lazy=True)

#----Association Table for Many-to-Many Relationship between Users and Listings----
class Favorites (db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    note = db.Column(db.String(200), default ="Want to book next month we gatchu you can always count on us!", nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ------Reviews and comments------
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='reviews')
    listing = db.relationship('Listing', backref='reviews')



