import csv
import datetime

from aiohttp import ClientSession
from sqlalchemy import insert, delete
from sqlalchemy.orm import Session

from models.phonebook import PhoneBookCategory, PhoneBookVersion, PhoneBook


async def insert_phone_book(db_session: Session):
    phonebook_url = "https://raw.githubusercontent.com/jil8885/API-for-ERICA/main/school/phone_book.csv"
    async with ClientSession() as session:
        async with session.get(phonebook_url) as response:
            reader = csv.reader((await response.text()).splitlines(), delimiter=",")
            phone_book_list = []
            category_list = []
            for row_index, (campus_id, category, name, phone) in enumerate(reader):
                if row_index == 0:
                    continue
                if category not in category_list:
                    category_list.append(category)
                phone_book_list.append({
                    "campus_id": campus_id,
                    "category_id": category_list.index(category),
                    "name": name,
                    "phone": phone,
                })
            category_dict = []
            for category_id, category_name in enumerate(category_list):
                category_dict.append({
                    "category_id": category_id,
                    "category_name": category_name,
                })
            # Delete all phone book data
            delete_phone_book_statement = delete(PhoneBook)
            db_session.execute(delete_phone_book_statement)
            delete_phone_book_category_statement = delete(PhoneBookCategory)
            db_session.execute(delete_phone_book_category_statement)
            delete_version_statement = delete(PhoneBookVersion)
            db_session.execute(delete_version_statement)
            db_session.commit()
            # Insert new phone book data
            now = datetime.datetime.now().astimezone(tz=datetime.timezone(datetime.timedelta(hours=9)))
            insert_version_statement = insert(PhoneBookVersion).values({
                "version_id": 1,
                "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": now,
            })
            db_session.execute(insert_version_statement)
            insert_category_statement = insert(PhoneBookCategory).values(category_dict)
            db_session.execute(insert_category_statement)
            db_session.commit()
            insert_statement = insert(PhoneBook).values(phone_book_list)
            db_session.execute(insert_statement)
            db_session.commit()
