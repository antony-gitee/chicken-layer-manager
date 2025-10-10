# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Chicken(db.Model):
    __tablename__ = "chickens"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    egg_logs = db.relationship("EggLog", backref="chicken", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "age": self.age,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class EggLog(db.Model):
    __tablename__ = "egg_logs"
    id = db.Column(db.Integer, primary_key=True)
    chicken_id = db.Column(db.Integer, db.ForeignKey("chickens.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "chicken_id": self.chicken_id,
            "date": self.date.isoformat() if self.date else None,
            "count": self.count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class FeedingLog(db.Model):
    __tablename__ = "feeding_logs"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time)
    feed_type = db.Column(db.String(100))
    water = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time.isoformat() if self.time else None,
            "feed_type": self.feed_type,
            "water": self.water,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
