import os
from src.helpers.auth import check_encrypted_password, decode_token, encrypt_password, generate_token
from src.models.user import User
from src.extensions import db


def resolve_users(obj, info):
    try:
        users = [user.to_dict() for user in User.query.all()]
        payload = {
            "success": True,
            "data": users
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload

def resolve_create_user(obj, info, name, email, password):
    try:
        user = User(
            name=name,
            email=email,
            password=encrypt_password(password)
        )
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "data": user.to_dict()
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload

def resolve_login(obj, info, email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            payload = {
                "success": False,
                "errors": ["Invalid request"]
            }
        is_valid = check_encrypted_password(password=password, hashed_password=user.password)

        if not is_valid:
            payload = {
                "success": False,
                "errors": ["Invalid request"]
            }
        token = generate_token(id=user.id, secret=os.getenv("SECRET_KEY"))
        payload = {
            "success": True,
            "data": user.to_dict(),
            "token": token
        }

    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload