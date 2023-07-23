# External Imports
from flask import Flask
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate

# Internal Imports
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from .models import db as root_db, login_manager, ma
from .helpers import JSONEncoder


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = "site.home"

ma.init_app(app)
app.json_encoder = JSONEncoder

CORS(app)

