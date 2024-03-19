from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class Restaurant(BaseModel):
    __tablename__ = "restaurant"
    campus_id: Mapped[int] = mapped_column(nullable=False)
    restaurant_id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_name: Mapped[str] = mapped_column(String(30), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    breakfast_time: Mapped[str] = mapped_column(String(40), nullable=True)
    lunch_time: Mapped[str] = mapped_column(String(40), nullable=True)
    dinner_time: Mapped[str] = mapped_column(String(40), nullable=True)
