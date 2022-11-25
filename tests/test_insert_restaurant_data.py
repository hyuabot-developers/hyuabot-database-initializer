import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.restaurant import Restaurant
from scripts import insert_restaurant_data
from utils.database import get_db_engine


class TestInsertRestaurantData:
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
    async def test_insert_restaurant_data(self):
        connection = get_db_engine()
        session_constructor = sessionmaker(bind=connection)
        # Database session check
        session = session_constructor()

        # Insert restaurant data
        await insert_restaurant_data(session)
        # Check if the data is inserted
        restaurant_count = session.query(Restaurant).count()
        assert restaurant_count == 11
        for restaurant_item in session.query(Restaurant).all():  # type: Restaurant
            assert type(restaurant_item.restaurant_id) is int
            assert type(restaurant_item.restaurant_name) is str
            assert type(restaurant_item.campus_id) is int
            assert type(restaurant_item.latitude) is float
            assert type(restaurant_item.longitude) is float
