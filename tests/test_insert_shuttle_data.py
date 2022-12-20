import datetime

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.shuttle import ShuttlePeriod, ShuttlePeriodType, ShuttleHoliday, ShuttleStop, \
    CommuteShuttleRoute, CommuteShuttleStop, CommuteShuttleTimetable
from scripts import insert_shuttle_period_type, \
    insert_shuttle_period, insert_shuttle_stop, \
    insert_commute_shuttle_route, insert_commute_shuttle_stop, \
    insert_commute_shuttle_timetable
from utils.database import get_db_engine


class TestInsertShuttleData:
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
    async def test_insert_shuttle_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()

        # Insert shuttle period type
        await insert_shuttle_period_type(session)
        # Check if the data is inserted
        shuttle_period_type_count = session.query(ShuttlePeriodType).count()
        assert shuttle_period_type_count == 3
        for period_type_item in session.query(ShuttlePeriodType).all():  # type: ShuttlePeriod
            assert type(period_type_item.period_type) is str

        # Insert shuttle period
        await insert_shuttle_period(session)
        # Check if the data is inserted
        shuttle_period_count = session.query(ShuttlePeriod).count()
        assert shuttle_period_count > 0
        for period_item in session.query(ShuttlePeriod).all():  # type: ShuttlePeriod
            assert type(period_item.period_type) is str
            assert type(period_item.period_start) is datetime.datetime
            assert type(period_item.period_end) is datetime.datetime
        shuttle_holiday_count = session.query(ShuttleHoliday).count()
        assert shuttle_holiday_count > 0
        for holiday_item in session.query(ShuttleHoliday).all():  # type: ShuttleHoliday
            assert type(holiday_item.holiday_type) is str
            assert type(holiday_item.holiday_date) is datetime.date
            assert type(holiday_item.calendar_type) is str

        # Insert shuttle stop
        await insert_shuttle_stop(session)
        # Check if the data is inserted
        shuttle_stop_count = session.query(ShuttleStop).count()
        assert shuttle_stop_count == 7
        for stop_item in session.query(ShuttleStop).all():  # type: ShuttleStop
            assert type(stop_item.stop_name) is str
            assert type(stop_item.latitude) is float
            assert type(stop_item.longitude) is float

        session.close()

    @pytest.mark.asyncio
    async def test_insert_commute_shuttle_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()

        # Insert commute shuttle route
        await insert_commute_shuttle_route(session)
        # Check if the data is inserted
        commute_shuttle_route_count = session.query(CommuteShuttleRoute).count()
        assert commute_shuttle_route_count == 9
        for commute_shuttle_route_item in session.query(CommuteShuttleRoute).all():
            assert type(commute_shuttle_route_item.route_name) is str
            assert type(commute_shuttle_route_item.route_description_korean) is str
            assert type(commute_shuttle_route_item.route_description_english) is str

        # Insert commute shuttle stop
        await insert_commute_shuttle_stop(session)
        # Check if the data is inserted
        commute_shuttle_stop_count = session.query(CommuteShuttleStop).count()
        assert commute_shuttle_stop_count > 0
        for commute_shuttle_stop_item in session.query(CommuteShuttleStop).all():
            assert type(commute_shuttle_stop_item.stop_name) is str
            assert type(commute_shuttle_stop_item.latitude) is float
            assert type(commute_shuttle_stop_item.longitude) is float

        # Insert commute shuttle timetable
        await insert_commute_shuttle_timetable(session)
        # Check if the data is inserted
        for commute_shuttle_timetable_item in session.query(CommuteShuttleTimetable).all():
            assert type(commute_shuttle_timetable_item.route_name) is str
            assert type(commute_shuttle_timetable_item.stop_name) is str
            assert type(commute_shuttle_timetable_item.stop_order) is int
            assert type(commute_shuttle_timetable_item.departure_time) is datetime.time
