import datetime

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
    station_seq: Mapped[int] = mapped_column(nullable=False)
    cumulative_time: Mapped[datetime.timedelta] = mapped_column(nullable=False)


class SubwayStationTranslation(BaseModel):
    __tablename__ = "subway_station_translation"
    station_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    language: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
