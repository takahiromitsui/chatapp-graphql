from src.models.room import Room


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