from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class SubwayStation(BaseModel):
    __tablename__ = "subway_station"
    station_name: Mapped[str] = mapped_column(String(30), nullable=False, primary_key=True)


class SubwayRoute(BaseModel):
    __tablename__ = "subway_route"
    route_id: Mapped[int] = mapped_column(primary_key=True)
    route_name: Mapped[str] = mapped_column(String(30), nullable=False)


class SubwayRouteStation(BaseModel):
    __tablename__ = "subway_route_station"
    station_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    route_id: Mapped[int] = mapped_column(nullable=False)
    station_name: Mapped[str] = mapped_column(String(30), nullable=False)
    station_sequence: Mapped[int] = mapped_column(nullable=False)
    cumulative_time: Mapped[float] = mapped_column(nullable=False)
