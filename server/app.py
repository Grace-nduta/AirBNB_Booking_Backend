#!/usr/bin/env python3

from flask import Flask
from models import db, User, Booking, Listing, Favorites
from flask_migrate import Migrate
from views.user import user_bp
from views.host import host_blueprint
from views.guest import guest_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(host_blueprint)
app.register_blueprint(guest_blueprint)

# Views go here!




@app.route('/')
def home():
    return '<h1>Airbnb Booking</h1>'

   
if __name__ == '__main__':
    app.run(port=5555, debug=True)

