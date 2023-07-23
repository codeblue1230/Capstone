# External Imports
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import secrets
import uuid


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False, default = '')
    last_name = db.Column(db.String(150), nullable = False, default = '')
    email = db.Column(db.String(150), nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    mapmarkers = db.relationship('MapMarkers', backref = 'owner', lazy = True)

    def __init__(self, first_name, last_name, email, username, password):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = self.set_password(password)
        self.token = self.set_token()

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)

    def __repr__(self):
        return f"User {self.email} has been added."
    

class MapMarkers(db.Model):
    id = db.Column(db.String, primary_key = True)
    store_name = db.Column(db.String(100), nullable = False, default = '')
    address = db.Column(db.String(300), nullable = False, default = '')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, store_name, address, user_token):
        self.id = self.set_id()
        self.store_name = store_name
        self.address = address
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Address at {self.store_name} has been added to the database!"
    
class MapMarkersSchema(ma.Schema):
    class Meta:
        fields = ['id', 'store_name', 'address']

map_marker_schema = MapMarkersSchema()
map_markers_schema = MapMarkersSchema(many = True)