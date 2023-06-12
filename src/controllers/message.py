from src.models.message import Message


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