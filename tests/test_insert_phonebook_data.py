import datetime

import pytest as pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from models import BaseModel
from models.campus import Campus
from models.phonebook import PhoneBookVersion, PhoneBookCategory, PhoneBook
from scripts import insert_campus_data, insert_phone_book
from utils.database import get_db_engine


class TestInsertPhonebookData:
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
    async def test_insert_phonebook_data(self):
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

        # Insert phonebook data
        await insert_phone_book(session)
        # Check if the data is inserted
        phonebook_version_count = session.query(PhoneBookVersion).count()
        assert phonebook_version_count > 0
        for phonebook_version in session.query(PhoneBookVersion).all():  # type: PhoneBookVersion
            assert type(phonebook_version.version_id) is int
            assert type(phonebook_version.version_name) is str
            assert type(phonebook_version.created_at) is datetime.datetime

        phonebook_category_count = session.query(PhoneBookCategory).count()
        assert phonebook_category_count > 0
        for phonebook_category in session.query(PhoneBookCategory).all():  # type: PhoneBookCategory
            assert type(phonebook_category.category_id) is int
            assert type(phonebook_category.category_name) is str
        phonebook_count = session.query(PhoneBook).count()
        assert phonebook_count > 0
        for phonebook in session.query(PhoneBook).all():
            assert type(phonebook.phonebook_id) is int
            assert type(phonebook.category_id) is int
            assert type(phonebook.campus_id) is int
            assert type(phonebook.name) is str
            assert type(phonebook.phone) is str
