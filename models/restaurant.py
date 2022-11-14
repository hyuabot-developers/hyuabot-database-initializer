from sqlalchemy import Column
from sqlalchemy.sql import sqltypes

from models import BaseModel


class Restaurant(BaseModel):
    __tablename__ = "restaurant"
    campus_id = Column(sqltypes.Integer, nullable=False)
    restaurant_id = Column(sqltypes.Integer, primary_key=True)
    restaurant_name = Column(sqltypes.String(30), nullable=False)
    latitude = Column(sqltypes.Float, nullable=False)
    longitude = Column(sqltypes.Float, nullable=False)
