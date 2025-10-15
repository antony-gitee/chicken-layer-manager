from datetime import datetime
from extensions import db

class Chicken(db.Model):
    __tablename__ = "chickens"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    egg_logs = db.relationship("EggLog", backref="chicken", cascade="all, delete-orphan")
    feeding_logs = db.relationship("FeedingLog", backref="chicken", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "age": self.age,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

class EggLog(db.Model):
    __tablename__ = "egg_logs"
    id = db.Column(db.Integer, primary_key=True)
    chicken_id = db.Column(db.Integer, db.ForeignKey('chickens.id'), nullable=False)
    number_of_eggs = db.Column(db.Integer, nullable=False)
    date_collected = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "chicken_id": self.chicken_id,
            "number_of_eggs": self.number_of_eggs,
            "date_collected": self.date_collected.strftime("%Y-%m-%d %H:%M:%S") if self.date_collected else None,
        }

class FeedingLog(db.Model):
    __tablename__ = "feeding_logs"
    id = db.Column(db.Integer, primary_key=True)
    chicken_id = db.Column(db.Integer, db.ForeignKey('chickens.id'), nullable=False)
    feed_type = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "chicken_id": self.chicken_id,
            "feed_type": self.feed_type,
            "quantity": self.quantity,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S") if self.date else None,
        }
