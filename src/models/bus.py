import datetime

from sqlalchemy import PrimaryKeyConstraint, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class BusStop(BaseModel):
    __tablename__ = "bus_stop"
    stop_id: Mapped[int] = mapped_column(primary_key=True)
    stop_name: Mapped[str] = mapped_column(String(30), nullable=False)
    district_code: Mapped[int] = mapped_column(nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(15), nullable=False)
    region_name: Mapped[str] = mapped_column(String(10), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)


class BusRoute(BaseModel):
    __tablename__ = "bus_route"
    company_id: Mapped[int] = mapped_column(nullable=False)
    company_name: Mapped[str] = mapped_column(String(30), nullable=False)
    company_telephone: Mapped[str] = mapped_column(String(15), nullable=False)
    district_code: Mapped[int] = mapped_column(nullable=False)
    up_first_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    up_last_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    down_first_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    down_last_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    start_stop_id: Mapped[int] = mapped_column(nullable=False)
    end_stop_id: Mapped[int] = mapped_column(nullable=False)
    route_name: Mapped[str] = mapped_column(String(30), nullable=False)
    route_type_code: Mapped[str] = mapped_column(String(10), nullable=False)
    route_type_name: Mapped[str] = mapped_column(String(10), nullable=False)
    route_id: Mapped[int] = mapped_column(nullable=False, primary_key=True)


class BusRouteStop(BaseModel):
    __tablename__ = "bus_route_stop"
    __table_args__ = (PrimaryKeyConstraint("route_id", "stop_id", name="pk_bus_route_stop"),)
    route_id: Mapped[int] = mapped_column(nullable=False)
    stop_id: Mapped[int] = mapped_column(nullable=False)
    stop_sequence: Mapped[int] = mapped_column(nullable=False)
    start_stop_id: Mapped[int] = mapped_column(nullable=False)
