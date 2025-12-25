from sqlalchemy import Column, Integer, Text, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    price_per_night = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    bookings = relationship("Booking", cascade="all, delete", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    room = relationship("Room", back_populates="bookings")