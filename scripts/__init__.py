from typing import TYPE_CHECKING

from scripts.bus import insert_bus_stop, insert_bus_route, insert_bus_route_stop
from scripts.campus import insert_campus_data
from scripts.restaurant import insert_restaurant_data
from scripts.shuttle import *
from scripts.subway import insert_subway_route, insert_subway_station

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def initialize_shuttle_data(db_session: Session):
    await insert_shuttle_period_type(db_session)
    await insert_shuttle_period(db_session)
    await insert_shuttle_route(db_session)
    await insert_shuttle_stop(db_session)
    await insert_shuttle_route_stop(db_session)
    await insert_shuttle_timetable(db_session)


async def initialize_bus_data(db_session: Session):
    await insert_bus_stop(db_session)
    await insert_bus_route(db_session)
    await insert_bus_route_stop(db_session)


async def initialize_subway_data(db_session: Session):
    await insert_subway_route(db_session)
    await insert_subway_station(db_session)


async def initialize_campus_data(db_session: Session):
    await insert_campus_data(db_session)


async def initialize_restaurant_data(db_session: Session):
    await insert_restaurant_data(db_session)
