import asyncio
import os

from sqlalchemy.orm import sessionmaker

from scripts import initialize_shuttle_data, initialize_bus_data, initialize_subway_data, \
    initialize_campus_data, initialize_restaurant_data, initialize_phonebook_data, initialize_calendar_data, \
    initialize_commute_route_data, initialize_subway_station_facility_data
from utils.database import get_db_engine


async def main():
    connection = get_db_engine()
    session_constructor = sessionmaker(bind=connection)
    session = session_constructor()
    if session is None:
        raise RuntimeError("Failed to get db session")
    jobs = {
        "shuttle": initialize_shuttle_data,
        "bus": initialize_bus_data,
        "subway": initialize_subway_data,
        "campus": initialize_campus_data,
        "restaurant": initialize_restaurant_data,
        "phonebook": initialize_phonebook_data,
        "calendar": initialize_calendar_data,
        "commute_route": initialize_commute_route_data,
        "subway_facility": initialize_subway_station_facility_data,
    }
    configured = os.getenv("INITIALIZER_JOBS", "").strip()
    selected = [name.strip() for name in configured.split(",") if name.strip()] if configured else list(jobs)
    unknown = set(selected) - jobs.keys()
    if unknown:
        raise ValueError(f"Unknown INITIALIZER_JOBS values: {', '.join(sorted(unknown))}")
    try:
        await asyncio.gather(*(jobs[name](session) for name in selected))
    finally:
        session.close()

if __name__ == '__main__':
    asyncio.run(main())
