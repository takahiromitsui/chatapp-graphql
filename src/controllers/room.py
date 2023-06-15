import os
from src.helpers.auth import decode_token
from src.models.room import Room
from src.extensions import db
from src.models.user import User

def resolve_rooms(obj, info):
    try:
        rooms = [room.to_dict() for room in Room.query.all()]
        payload = {
            "success": True,
            "data": rooms
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload

def resolve_create_room(obj, info, name):
    try:
        room = Room(
            name=name
        )
        db.session.add(room)
        db.session.commit()
        payload = {
            "success": True,
            "data": room.to_dict()
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload

def resolve_rooms_by_user_id(obj, info):
    try:
        token = info.context["request"].headers.get("Authorization")
        if not token:
            raise Exception("Token is missing")
        
        decoded_token = decode_token(token, os.getenv("SECRET_KEY"))
        user_id = decoded_token["id"]

        user = User.query.get(user_id)
        rooms = [room.to_dict() for room in user.rooms]
        payload = {
            "success": True,
            "data": rooms
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload