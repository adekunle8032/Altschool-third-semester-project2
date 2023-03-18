from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config
from app.models import db
from app.schemas import ma
from app.utils import register_resources

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app, title='Student Management API', doc='/doc')

# Enable CORS
CORS(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize database and marshmallow
db.init_app(app)
ma.init_app(app)

# Register resources from utils
register_resources(api)

# Handle errors
@api.errorhandler(Exception)
def handle_error(e):
    code = 500
    if hasattr(e, 'status_code'):
        code = e.status_code
    return jsonify(error=str(e)), code

if __name__ == '__main__':
    app.run()
