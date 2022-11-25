import datetime

from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.orm import mapped_column, Mapped

from models import BaseModel


class ShuttlePeriodType(BaseModel):
    __tablename__ = "shuttle_period_type"
    period_type: Mapped[str] = mapped_column(String(20), nullable=False, primary_key=True)


class ShuttlePeriod(BaseModel):
    __tablename__ = "shuttle_period"
    __table_args__ = (PrimaryKeyConstraint("period_type", "period_start"),)
    period_type: Mapped[str] = mapped_column(String(20), nullable=False)
    period_start: Mapped[datetime.datetime] = mapped_column(nullable=False)
    period_end: Mapped[datetime.datetime] = mapped_column(nullable=False)


class ShuttleHoliday(BaseModel):
    __tablename__ = "shuttle_holiday"
    __table_args__ = (PrimaryKeyConstraint("holiday_date", "calendar_type"),)
    holiday_date: Mapped[datetime.date] = mapped_column(nullable=False)
    holiday_type: Mapped[str] = mapped_column(String(15), nullable=False)
    calendar_type: Mapped[str] = mapped_column(String(15), nullable=False)


class ShuttleRoute(BaseModel):
    __tablename__ = "shuttle_route"
    route_id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    route_name: Mapped[str] = mapped_column(String(15), nullable=False)
    route_description_korean: Mapped[str] = mapped_column(String(100), nullable=False)
    route_description_english: Mapped[str] = mapped_column(String(100), nullable=False)


class ShuttleStop(BaseModel):
    __tablename__ = "shuttle_stop"
    stop_name: Mapped[str] = mapped_column(String(15), nullable=False, primary_key=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)


class ShuttleRouteStop(BaseModel):
    __tablename__ = "shuttle_route_stop"
    __table_args__ = (PrimaryKeyConstraint('route_name', 'stop_name', name="pk_shuttle_route_stop"),)
    route_name: Mapped[str] = mapped_column(String(15), nullable=False)
    stop_name: Mapped[str] = mapped_column(String(15), nullable=False)
    stop_order: Mapped[int] = mapped_column(nullable=False)
    cumulative_time: Mapped[int] = mapped_column(nullable=False)


class ShuttleTimetable(BaseModel):
    __tablename__ = "shuttle_timetable"
    __table_args__ = (PrimaryKeyConstraint('route_name', 'period_type', 'weekday', 'departure_time',
                                           name="pk_shuttle_timetable"),)
    route_name: Mapped[str] = mapped_column(String(15), nullable=False)
    period_type: Mapped[str] = mapped_column(String(20), nullable=False)
    weekday: Mapped[bool] = mapped_column(nullable=False)
    departure_time: Mapped[datetime.time] = mapped_column(nullable=False)
    start_stop: Mapped[str] = mapped_column(String(15), nullable=False)


class CommuteShuttleRoute(BaseModel):
    __tablename__ = "commute_shuttle_route"
    route_name: Mapped[str] = mapped_column(String(15), primary_key=True)
    route_description_korean: Mapped[str] = mapped_column(String(100), nullable=False)
    route_description_english: Mapped[str] = mapped_column(String(100), nullable=False)


class CommuteShuttleStop(BaseModel):
    __tablename__ = "commute_shuttle_stop"
    stop_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)


class CommuteShuttleTimetable(BaseModel):
    __tablename__ = "commute_shuttle_timetable"
    __table_args__ = (PrimaryKeyConstraint('route_name', 'stop_name',
                                           name="pk_commute_shuttle_timetable"),)
    route_name: Mapped[str] = mapped_column(String(15), nullable=False)
    stop_name: Mapped[str] = mapped_column(String(50), nullable=False)
    stop_order: Mapped[int] = mapped_column(nullable=False)
    departure_time: Mapped[datetime.time] = mapped_column(nullable=False)
