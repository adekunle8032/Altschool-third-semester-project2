from functools import wraps
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_claims,
    get_current_user,
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
)

from app.models import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        claims = get_jwt_claims()
        current_user = get_current_user()

        if not claims["is_admin"] or not current_user:
            return {"message": "Admins only! Unauthorized access!"}, 403

        return fn(*args, **kwargs)

    return wrapper


def is_owner_or_admin(model_class):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            current_user = get_current_user()

            if not current_user:
                return {"message": "Unauthorized access!"}, 401

            model_id = kwargs.get("id")
            model = model_class.query.get(model_id)

            if not model:
                return {"message": f"{model_class.__name__} not found!"}, 404

            if model.user_id != current_user.id and not current_user.is_admin:
                return {"message": "Unauthorized access!"}, 401

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def authenticate(username, password):
    user = User.get_by_username(username)

    if user and user.is_active and user.check_password(password):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}

    return None, 401


@jwt_refresh_token_required
def refresh_token():
    current_user = get_current_user()
    access_token = create_access_token(identity=current_user.id, fresh=False)

    return {"access_token": access_token}
