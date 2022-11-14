from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.sql import sqltypes

from models import BaseModel


class BusStop(BaseModel):
    __tablename__ = "bus_stop"
    stop_id = Column(sqltypes.Integer, primary_key=True)
    stop_name = Column(sqltypes.String(30), nullable=False)
    district_code = Column(sqltypes.Integer, nullable=False)
    mobile_number = Column(sqltypes.String(15), nullable=False)
    region_name = Column(sqltypes.String(10), nullable=False)
    latitude = Column(sqltypes.Float, nullable=False)
    longitude = Column(sqltypes.Float, nullable=False)


class BusRoute(BaseModel):
    __tablename__ = "bus_route"
    company_id = Column(sqltypes.Integer, nullable=False)
    company_name = Column(sqltypes.String(30), nullable=False)
    company_telephone = Column(sqltypes.String(15), nullable=False)
    district_code = Column(sqltypes.Integer, nullable=False)
    up_first_time = Column(sqltypes.Time, nullable=False)
    up_last_time = Column(sqltypes.Time, nullable=False)
    down_first_time = Column(sqltypes.Time, nullable=False)
    down_last_time = Column(sqltypes.Time, nullable=False)
    start_stop_id = Column(sqltypes.Integer, nullable=False)
    end_stop_id = Column(sqltypes.Integer, nullable=False)
    route_name = Column(sqltypes.String(30), nullable=False)
    route_type_code = Column(sqltypes.String(10), nullable=False)
    route_type_name = Column(sqltypes.String(10), nullable=False)
    route_id = Column(sqltypes.Integer, nullable=False, primary_key=True)


class BusRouteStop(BaseModel):
    __tablename__ = "bus_route_stop"
    __table_args__ = (PrimaryKeyConstraint("route_id", "stop_id"),)
    route_id = Column(sqltypes.Integer, nullable=False)
    stop_id = Column(sqltypes.Integer, nullable=False)
    stop_sequence = Column(sqltypes.Integer, nullable=False)
