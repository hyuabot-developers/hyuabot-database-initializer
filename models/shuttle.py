from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.sql import sqltypes

from models import BaseModel


class ShuttlePeriodType(BaseModel):
    __tablename__ = "shuttle_period_type"
    period_type = Column(sqltypes.String(20), nullable=False, primary_key=True)


class ShuttlePeriod(BaseModel):
    __tablename__ = "shuttle_period"
    __table_args__ = (PrimaryKeyConstraint("period_type", "period_start"),)
    period_type = Column(sqltypes.String(15), nullable=False)
    period_start = Column(sqltypes.DateTime, nullable=False)
    period_end = Column(sqltypes.DateTime, nullable=False)


class ShuttleHoliday(BaseModel):
    __tablename__ = "shuttle_holiday"
    __table_args__ = (PrimaryKeyConstraint("holiday_date", "calendar_type"),)
    holiday_date = Column(sqltypes.Date, nullable=False)
    holiday_type = Column(sqltypes.String(15), nullable=False)
    calendar_type = Column(sqltypes.String(15), nullable=False)


class ShuttleRoute(BaseModel):
    __tablename__ = "shuttle_route"
    route_id = Column(sqltypes.Integer, nullable=False, primary_key=True)
    route_name = Column(sqltypes.String(15), nullable=False)


class ShuttleStop(BaseModel):
    __tablename__ = "shuttle_stop"
    stop_name = Column(sqltypes.String(15), nullable=False, primary_key=True)
    latitude = Column(sqltypes.Float, nullable=False)
    longitude = Column(sqltypes.Float, nullable=False)


class ShuttleRouteStop(BaseModel):
    __tablename__ = "shuttle_route_stop"
    __table_args__ = (PrimaryKeyConstraint('route_name', 'stop_name'),)
    route_name = Column(sqltypes.String(15), nullable=False)
    stop_name = Column(sqltypes.String(15), nullable=False)
    stop_order = Column(sqltypes.Integer, nullable=False)


class ShuttleTimetable(BaseModel):
    __tablename__ = "shuttle_timetable"
    __table_args__ = (PrimaryKeyConstraint('route_name', 'period_type', 'weekday', 'departure_time'),)
    route_name = Column(sqltypes.String(15), nullable=False)
    period_type = Column(sqltypes.String(15), nullable=False)
    weekday = Column(sqltypes.Boolean, nullable=False)
    departure_time = Column(sqltypes.Time, nullable=False)
    start_stop = Column(sqltypes.String(15), nullable=False)
