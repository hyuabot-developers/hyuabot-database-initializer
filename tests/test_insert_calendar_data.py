import datetime

import pytest as pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.calendar import CalendarVersion, CalendarCategory, Calendar
from scripts import insert_calendar_data
from utils.database import get_db_engine


class TestInsertCalendarData:
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
    async def test_insert_calendar_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()
        # Insert calendar data
        await insert_calendar_data(session)
        # Check if the data is inserted
        calendar_version_count = session.query(CalendarVersion).count()
        assert calendar_version_count == 1
        for calendar_version in session.query(CalendarVersion).all():
            assert type(calendar_version.version_id) is int
            assert type(calendar_version.version_name) is str
            assert type(calendar_version.created_at) is datetime.datetime

        calendar_category_count = session.query(CalendarCategory).count()
        assert calendar_category_count == 1
        for calendar_category in session.query(CalendarCategory).all():
            assert type(calendar_category.category_id) is int
            assert type(calendar_category.category_name) is str

        calendar_count = session.query(Calendar).count()
        assert calendar_count > 0
        for calendar in session.query(Calendar).all():
            assert type(calendar.academic_calendar_id) is int
            assert type(calendar.category_id) is int
            assert type(calendar.title) is str
            assert type(calendar.description) is str
            assert type(calendar.start_date) is datetime.date
            assert type(calendar.end_date) is datetime.date
