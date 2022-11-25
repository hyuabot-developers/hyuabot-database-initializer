import datetime

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.bus import BusStop, BusRoute, BusRouteStop
from scripts import insert_bus_stop, insert_bus_route, insert_bus_route_stop
from utils.database import get_db_engine


class TestInsertBusData:
    connection: Engine | None = None
    session_constructor = None
    session: Session | None = None

    @classmethod
    def setup_class(cls):
        cls.connection = get_db_engine()
        cls.session_constructor = sessionmaker(bind=cls.connection)
        # Database session check
        cls.session = cls.session_constructor()
        assert cls.session is not None
        # Migration schema check
        BaseModel.metadata.create_all(cls.connection)

    @pytest.mark.asyncio
    async def test_insert_bus_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()

        # Insert bus stop
        await insert_bus_stop(session)
        # Check if the data is inserted
        bus_stop_count = session.query(BusStop).count()
        assert bus_stop_count > 0
        for bus_stop_item in session.query(BusStop).all():  # type: BusStop
            assert type(bus_stop_item.stop_id) is int
            assert type(bus_stop_item.stop_name) is str
            assert type(bus_stop_item.district_code) is int
            assert type(bus_stop_item.mobile_number) is str
            assert type(bus_stop_item.region_name) is str
            assert type(bus_stop_item.latitude) is float
            assert type(bus_stop_item.longitude) is float

        # Insert bus route
        await insert_bus_route(session)
        # Check if the data is inserted
        bus_route_count = session.query(BusRoute).count()
        assert bus_route_count > 0
        for bus_route_item in session.query(BusRoute).all():  # type: BusRoute
            assert type(bus_route_item.company_id) is int
            assert type(bus_route_item.company_name) is str
            assert type(bus_route_item.company_telephone) is str
            assert type(bus_route_item.district_code) is int
            assert type(bus_route_item.up_first_time) is datetime.time
            assert type(bus_route_item.up_last_time) is datetime.time
            assert type(bus_route_item.down_first_time) is datetime.time
            assert type(bus_route_item.down_last_time) is datetime.time
            assert type(bus_route_item.start_stop_id) is int
            assert type(bus_route_item.end_stop_id) is int
            assert type(bus_route_item.route_id) is int
            assert type(bus_route_item.route_name) is str
            assert type(bus_route_item.route_type_code) is str
            assert type(bus_route_item.route_type_name) is str

        # Insert bus route stop
        await insert_bus_route_stop(session)
        # Check if the data is inserted
        bus_route_stop_count = session.query(BusRouteStop).count()
        assert bus_route_stop_count == 11
        for bus_route_stop_item in session.query(BusRouteStop).all():  # type: BusRouteStop
            assert type(bus_route_stop_item.route_id) is int
            assert type(bus_route_stop_item.stop_id) is int
            assert type(bus_route_stop_item.stop_sequence) is int
