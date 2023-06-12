from src.extensions import db

user_room_association = db.Table(
    'user_room',
    db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('room_id', db.String, db.ForeignKey('room.id'), primary_key=True)
)