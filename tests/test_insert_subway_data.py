import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.subway import SubwayRoute, SubwayStation
from scripts import insert_subway_route, insert_subway_station
from utils.database import get_db_engine


class TestInsertSubwayData:
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
    async def test_insert_subway_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()

        # Insert subway route
        await insert_subway_route(session)
        # Check if the data is inserted
        subway_route_count = session.query(SubwayRoute).count()
        assert subway_route_count == 16
        for route_item in session.query(SubwayRoute).all():  # type: SubwayRoute
            assert type(route_item.route_id) is int
            assert type(route_item.route_name) is str

        # Insert subway station
        await insert_subway_station(session)
        # Check if the data is inserted
        subway_station_count = session.query(SubwayStation).count()
        assert subway_station_count > 0
        for station_item in session.query(SubwayStation).all():  # type: SubwayStation
            assert type(station_item.station_name) is str
