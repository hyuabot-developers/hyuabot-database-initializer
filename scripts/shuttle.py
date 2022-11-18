import asyncio
import csv
import json
from datetime import datetime, timezone, timedelta

from aiohttp import ClientSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.shuttle import ShuttlePeriodType, ShuttlePeriod, ShuttleRoute, ShuttleStop, \
    ShuttleRouteStop, ShuttleHoliday, ShuttleTimetable


async def insert_shuttle_period_type(db_session: Session):
    period_type_list = [
        dict(period_type="semester"),
        dict(period_type="vacation"),
        dict(period_type="vacation_session"),
    ]
    insert_statement = insert(ShuttlePeriodType).values(period_type_list)
    insert_statement = insert_statement.on_conflict_do_nothing()
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_shuttle_period(db_session: Session):
    url = "https://raw.githubusercontent.com/hyuabot-developers/hyuabot-shuttle-timetable/main/date.json"

    period_items = []
    holiday_items = []
    now = datetime.now(tz=timezone(timedelta(hours=9)))
    async with ClientSession() as session:
        async with session.get(url) as response:
            date_json = json.loads(await response.text())
            for holiday in date_json['holiday']:
                month, day = holiday.split('/')
                if now.month > int(month) or (now.month == int(month) and now.day > int(day)):
                    year = now.year + 1
                else:
                    year = now.year
                holiday_items.append(
                    dict(
                        holiday_type="weekends",
                        holiday_date=datetime.fromisoformat(
                            f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"),
                        calendar_type="solar",
                    ))
            for calendar_type, holiday_list in date_json['halt'].items():
                for holiday in holiday_list:
                    month, day = holiday.split('/')
                    if calendar_type == "lunar":
                        year = now.year
                    else:
                        if now.month > int(month) or (now.month == int(month) and now.day > int(day)):
                            year = now.year + 1
                        else:
                            year = now.year
                    holiday_items.append(
                        dict(
                            holiday_type="halt",
                            holiday_date=datetime.fromisoformat(
                                f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"),
                            calendar_type=calendar_type,
                        ))
            for period in ["semester", "vacation", "vacation_session"]:
                for period_item in date_json[period]:
                    start_date = datetime.strptime(period_item['start'], "%m/%d") \
                        .replace(year=now.year, hour=0, minute=0, second=0)
                    end_date = datetime.strptime(period_item['end'], "%m/%d") \
                        .replace(year=now.year, hour=23, minute=59, second=59)
                    start_date = datetime.fromisoformat(
                        f"{year}-{str(start_date.month).zfill(2)}-{str(start_date.day).zfill(2)}T00:00:00+09:00")
                    end_date = datetime.fromisoformat(
                        f"{year}-{str(end_date.month).zfill(2)}-{str(end_date.day).zfill(2)}T23:59:59+09:00")
                    if start_date < end_date:
                        if now.month > int(end_date.month) or \
                                (now.month == int(end_date.month) and now.day > int(end_date.day)):
                            start_date = start_date.replace(year=now.year + 1)
                            end_date = end_date.replace(year=now.year + 1)
                    else:
                        if now.month < int(end_date.month) or \
                                (now.month == int(end_date.month) and now.day < int(end_date.day)):
                            start_date = start_date.replace(year=now.year - 1)
                        else:
                            end_date = end_date.replace(year=now.year + 1)
                    period_items.append(
                        dict(
                            period_type=period,
                            period_start=start_date,
                            period_end=end_date,
                        ))
            db_session.query(ShuttleHoliday).delete()
            db_session.bulk_insert_mappings(ShuttleHoliday, holiday_items)
            db_session.query(ShuttlePeriod).delete()
            db_session.bulk_insert_mappings(ShuttlePeriod, period_items)
            db_session.commit()


async def insert_shuttle_route(db_session: Session):
    route_list = [
        dict(route_name="DH"),
        dict(route_name="DH(short)"),
        dict(route_name="DY"),
        dict(route_name="DY(short)"),
        dict(route_name="C"),
        dict(route_name="C(short)"),
        dict(route_name="DJ"),
    ]
    insert_statement = insert(ShuttleRoute).values(route_list)
    insert_statement = insert_statement.on_conflict_do_nothing()
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_shuttle_stop(db_session: Session):
    stop_list = [
        dict(stop_name="dormitory_o", latitude=37.29339607529377, longitude=126.83630604103446),
        dict(stop_name="shuttlecock_o", latitude=37.29875417910844, longitude=126.83784054072336),
        dict(stop_name="station", latitude=37.308494476826155, longitude=126.85310236423418),
        dict(stop_name="terminal", latitude=37.31945164682341, longitude=126.8455453372041),
        dict(stop_name="shuttlecock_i", latitude=37.2995897, longitude=126.8372216),
        dict(stop_name="dormitory_i", latitude=37.29339607529377, longitude=126.83630604103446),
        dict(stop_name="jungang_stn", latitude=37.3147818, longitude=126.8397399),
    ]
    insert_statement = insert(ShuttleStop).values(stop_list)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["stop_name"],
        set_=dict(
            latitude=insert_statement.excluded.latitude, longitude=insert_statement.excluded.longitude),
    )
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_shuttle_route_stop(db_session: Session):
    route_stop_list = [
        dict(route_name="DH", stop_name="dormitory_o", stop_order=0),
        dict(route_name="DH", stop_name="shuttlecock_o", stop_order=1),
        dict(route_name="DH", stop_name="station", stop_order=2),
        dict(route_name="DH", stop_name="shuttlecock_i", stop_order=3),
        dict(route_name="DH", stop_name="dormitory_i", stop_order=4),
        dict(route_name="DH(short)", stop_name="shuttlecock_o", stop_order=0),
        dict(route_name="DH(short)", stop_name="station", stop_order=1),
        dict(route_name="DH(short)", stop_name="shuttlecock_i", stop_order=2),
        dict(route_name="DY", stop_name="dormitory_o", stop_order=0),
        dict(route_name="DY", stop_name="shuttlecock_o", stop_order=1),
        dict(route_name="DY", stop_name="terminal", stop_order=2),
        dict(route_name="DY", stop_name="shuttlecock_i", stop_order=3),
        dict(route_name="DY", stop_name="dormitory_i", stop_order=4),
        dict(route_name="DY(short)", stop_name="shuttlecock_o", stop_order=0),
        dict(route_name="DY(short)", stop_name="terminal", stop_order=1),
        dict(route_name="DY(short)", stop_name="shuttlecock_i", stop_order=2),
        dict(route_name="C", stop_name="dormitory_o", stop_order=0),
        dict(route_name="C", stop_name="shuttlecock_o", stop_order=1),
        dict(route_name="C", stop_name="station", stop_order=2),
        dict(route_name="C", stop_name="terminal", stop_order=3),
        dict(route_name="C", stop_name="shuttlecock_i", stop_order=4),
        dict(route_name="C", stop_name="dormitory_i", stop_order=5),
        dict(route_name="C(short)", stop_name="shuttlecock_o", stop_order=0),
        dict(route_name="C(short)", stop_name="station", stop_order=1),
        dict(route_name="C(short)", stop_name="shuttlecock_i", stop_order=2),
        dict(route_name="DJ", stop_name="dormitory_o", stop_order=0),
        dict(route_name="DJ", stop_name="shuttlecock_o", stop_order=1),
        dict(route_name="DJ", stop_name="station", stop_order=2),
        dict(route_name="DJ", stop_name="jungang_stn", stop_order=3),
        dict(route_name="DJ", stop_name="shuttlecock_i", stop_order=4),
        dict(route_name="DJ", stop_name="dormitory_i", stop_order=5),
    ]
    insert_statement = insert(ShuttleRouteStop).values(route_stop_list)
    insert_statement = insert_statement.on_conflict_do_update(
        constraint="pk_shuttle_route_stop",
        set_=dict(stop_order=insert_statement.excluded.stop_order),
    )
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_shuttle_timetable(db_session: Session):
    term_keys = ["semester", "vacation", "vacation_session"]
    day_keys = ["week", "weekend"]

    tasks = []
    db_session.query(ShuttleTimetable).delete()
    for term in term_keys:
        for day in day_keys:
            tasks.append(fetch_shuttle_timetable(db_session, term, day))
    await asyncio.gather(*tasks)
    db_session.commit()


async def fetch_shuttle_timetable(db_session: Session, period: str, day: str):
    base_url = "https://raw.githubusercontent.com/hyuabot-developers/hyuabot-shuttle-timetable/main"
    url = f"{base_url}/{period}/{day}.csv"
    day_dict = {"week": "weekdays", "weekend": "weekends"}
    timetable: list[dict] = []
    async with ClientSession() as session:
        async with session.get(url) as response:
            reader = csv.reader((await response.text()).splitlines(), delimiter=",")
            for shuttle_type, shuttle_time, shuttle_start_stop in reader:
                if shuttle_start_stop == "Shuttlecock":
                    shuttle_type = f"{shuttle_type}(short)"
                    shuttle_start_stop = "shuttlecock_o"
                elif shuttle_start_stop == "Dormitory":
                    shuttle_start_stop = "dormitory_o"
                timetable.append(
                    dict(
                        route_name=shuttle_type,
                        period_type=period,
                        weekday=day_dict[day] == "weekdays",
                        start_stop=shuttle_start_stop,
                        departure_time=datetime.fromisoformat(f"1998-12-12T{shuttle_time}:00+09:00"),
                    ),
                )
    insert_statement = insert(ShuttleTimetable).values(timetable)
    insert_statement = insert_statement.on_conflict_do_update(
        constraint="pk_shuttle_timetable",
        set_=dict(start_stop=insert_statement.excluded.start_stop)
    )
    db_session.execute(insert_statement)
    db_session.commit()
