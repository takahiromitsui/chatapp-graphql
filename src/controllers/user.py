from src.models.user import User


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