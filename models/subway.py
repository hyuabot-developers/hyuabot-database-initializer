from sqlalchemy import Column
from sqlalchemy.sql import sqltypes

from models import BaseModel


class SubwayStation(BaseModel):
    __tablename__ = "subway_station"
    station_name = Column(sqltypes.String(30), nullable=False, primary_key=True)


class SubwayRoute(BaseModel):
    __tablename__ = "subway_route"
    route_id = Column(sqltypes.Integer, primary_key=True)
    route_name = Column(sqltypes.String(30), nullable=False)


class SubwayRouteStation(BaseModel):
    __tablename__ = "subway_route_station"
    station_id = Column(sqltypes.String(10), primary_key=True)
    route_id = Column(sqltypes.Integer, nullable=False)
    station_name = Column(sqltypes.String(30), nullable=False)
    station_sequence = Column(sqltypes.Integer, nullable=False)
    cumulative_time = Column(sqltypes.Integer, nullable=False)
