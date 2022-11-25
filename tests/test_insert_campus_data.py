import pytest as pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.campus import Campus
from scripts import insert_campus_data
from utils.database import get_db_engine


class TestInsertCampusData:
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
    async def test_insert_campus_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()
        # Get list to fetch
        await insert_campus_data(session)

        # Check if the data is inserted
        campus_item_count = session.query(Campus).count()
        assert campus_item_count == 2
        for campus in session.query(Campus).all():  # type: Campus
            assert type(campus.campus_id) is int
            assert type(campus.campus_name) is str
