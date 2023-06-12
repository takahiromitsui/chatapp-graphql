from src.models.room import Room
from src.extensions import db

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