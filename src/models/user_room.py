from src.main import db

user_room_association = db.Table(
    'user_room',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True)
)

class UserRoom(db.Model):
    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    room_id = db.Column(db.String, db.ForeignKey('room.id'), primary_key=True)
    user = db.relationship("User", back_populates="rooms")
    room = db.relationship("Room", back_populates="users")
    messages = db.relationship('Message', backref='user_room')
    
    def to__dict__(self):
        return {
            "user_id": self.user_id,
            "room_id": self.room_id
        }