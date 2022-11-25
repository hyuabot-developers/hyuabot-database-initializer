import asyncio

from sqlalchemy.orm import sessionmaker

from scripts import initialize_shuttle_data, initialize_bus_data, initialize_subway_data, \
    initialize_campus_data, initialize_restaurant_data
from utils.database import get_db_engine


async def main():
    connection = get_db_engine()
    session_constructor = sessionmaker(bind=connection)
    session = session_constructor()
    if session is None:
        raise RuntimeError("Failed to get db session")
    job_list = [
        initialize_shuttle_data(session),
        initialize_bus_data(session),
        initialize_subway_data(session),
        initialize_campus_data(session),
        initialize_restaurant_data(session),
    ]
    await asyncio.gather(*job_list)
    session.close()

if __name__ == '__main__':
    asyncio.run(main())
