from sqlalchemy import Column
from sqlalchemy.sql import sqltypes

from models import BaseModel


class ReadingRoom(BaseModel):
    __tablename__ = "reading_room"
    campus_id = Column(sqltypes.Integer, nullable=False)
    room_id = Column(sqltypes.Integer, primary_key=True)
    room_name = Column(sqltypes.String(30), nullable=False)
    is_active = Column(sqltypes.Boolean, nullable=False)
    is_reservable = Column(sqltypes.Boolean, nullable=False)
    total_seat_count = Column(sqltypes.Integer, nullable=False)
    total_active_seat_count = Column(sqltypes.Integer, nullable=False)
    occupied_seat_count = Column(sqltypes.Integer, nullable=False)
    available_seat_count = Column(sqltypes.Integer, nullable=False)
