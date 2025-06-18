#!/usr/bin/env python3

from flask import Flask
from server.models import db, User, Booking, Listing, Favorites, Review
from flask_migrate import Migrate
from server.views.user import user_bp
from server.views.host import host_blueprint
from server.views.listing import listing_bp
from server.views.admin import admin_blueprint
from server.views.booking import booking_bp
from server.views.favorite import favorite_bp
from server.views.review import review_bp
from server.views.auth import auth_bp
import os
from datetime import timedelta

# JWT importations
from flask_jwt_extended import JWTManager


app = Flask(__name__)

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "app.db")}'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "wyhjmmxmjhhdytd" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)  
jwt = JWTManager(app)
jwt.init_app(app)

# Views go here!
app.register_blueprint(user_bp)
app.register_blueprint(host_blueprint)
app.register_blueprint(listing_bp)
app.register_blueprint(admin_blueprint)
app.register_blueprint(booking_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(review_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def home():
    return '<h1>Airbnb Booking</h1>'

   
if __name__ == '__main__':
    app.run(port=5555, debug=True)

