from src.models.message import Message
from src.extensions import db


def resolve_messages(obj, info):
    try:
        messages = [message.to_dict() for message in Message.query.all()]
        payload = {
            "success": True,
            "data": messages
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload

def resolve_create_message(obj, info, content, user_id, room_id):
    try:
        message = Message(
            content=content,
            user_id=user_id,
            room_id=room_id
        )
        print(message)
        db.session.commit()
        payload = {
            "success": True,
            "data": message.to_dict()
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload