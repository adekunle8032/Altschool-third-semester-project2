from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    JWTManager,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User

jwt = JWTManager()


def init_app(app):
    jwt.init_app(app)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.get_by_id(identity)


def authenticate(username, password):
    user = User.get_by_username(username)

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}

    return None, 401


@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, fresh=False)

    return {"access_token": access_token}
