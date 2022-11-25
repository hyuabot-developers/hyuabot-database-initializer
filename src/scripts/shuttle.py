import asyncio
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone, timedelta

from aiohttp import ClientSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.shuttle import ShuttlePeriodType, ShuttlePeriod, ShuttleRoute, ShuttleStop, \
    ShuttleRouteStop, ShuttleHoliday, ShuttleTimetable, CommuteShuttleRoute, CommuteShuttleStop, \
    CommuteShuttleTimetable


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
            db_session.execute(insert(ShuttleHoliday).values(holiday_items))
            db_session.query(ShuttlePeriod).delete()
            db_session.execute(insert(ShuttlePeriod).values(period_items))
            db_session.commit()


async def insert_shuttle_route(db_session: Session):
    route_list = [
        dict(route_name="DH",
             route_description_korean="한대앞 직행",
             route_description_english="Direct to Station"),
        dict(route_name="DHC",
             route_description_korean="한대앞 직행(등교 시간대)",
             route_description_english="Direct to Station(Commute)"),
        dict(route_name="DY",
             route_description_korean="예술인 직행",
             route_description_english="Direct to Terminal"),
        dict(route_name="DYC",
             route_description_korean="예술인 직행(등교 시간대)",
             route_description_english="Direct to Terminal(Commute)"),
        dict(route_name="C",
             route_description_korean="순환",
             route_description_english="Circular"),
        dict(route_name="CC",
             route_description_korean="순환(등교 시간대)",
             route_description_english="Circular(Commute)"),
        dict(route_name="DJ",
             route_description_korean="한대앞 직행(중앙역 경유)",
             route_description_english="Direct to Station(Jungang Station)"),
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
        dict(route_name="DH", stop_name="dormitory_o", stop_order=0, cumulative_time=-5),
        dict(route_name="DH", stop_name="shuttlecock_o", stop_order=1, cumulative_time=0),
        dict(route_name="DH", stop_name="station", stop_order=2, cumulative_time=10),
        dict(route_name="DH", stop_name="shuttlecock_i", stop_order=3, cumulative_time=20),
        dict(route_name="DH", stop_name="dormitory_i", stop_order=4, cumulative_time=25),
        dict(route_name="DHC", stop_name="shuttlecock_o", stop_order=0, cumulative_time=0),
        dict(route_name="DHC", stop_name="station", stop_order=1, cumulative_time=10),
        dict(route_name="DHC", stop_name="shuttlecock_i", stop_order=2, cumulative_time=20),
        dict(route_name="DY", stop_name="dormitory_o", stop_order=0, cumulative_time=-5),
        dict(route_name="DY", stop_name="shuttlecock_o", stop_order=1, cumulative_time=0),
        dict(route_name="DY", stop_name="terminal", stop_order=2, cumulative_time=10),
        dict(route_name="DY", stop_name="shuttlecock_i", stop_order=3, cumulative_time=20),
        dict(route_name="DY", stop_name="dormitory_i", stop_order=4, cumulative_time=25),
        dict(route_name="DYC", stop_name="shuttlecock_o", stop_order=0, cumulative_time=0),
        dict(route_name="DYC", stop_name="terminal", stop_order=1, cumulative_time=10),
        dict(route_name="DYC", stop_name="shuttlecock_i", stop_order=2, cumulative_time=20),
        dict(route_name="C", stop_name="dormitory_o", stop_order=0, cumulative_time=-5),
        dict(route_name="C", stop_name="shuttlecock_o", stop_order=1, cumulative_time=0),
        dict(route_name="C", stop_name="station", stop_order=2, cumulative_time=10),
        dict(route_name="C", stop_name="terminal", stop_order=3, cumulative_time=15),
        dict(route_name="C", stop_name="shuttlecock_i", stop_order=4, cumulative_time=25),
        dict(route_name="C", stop_name="dormitory_i", stop_order=5, cumulative_time=30),
        dict(route_name="CC", stop_name="shuttlecock_o", stop_order=0, cumulative_time=0),
        dict(route_name="CC", stop_name="station", stop_order=1, cumulative_time=10),
        dict(route_name="CC", stop_name="terminal", stop_order=2, cumulative_time=15),
        dict(route_name="CC", stop_name="shuttlecock_i", stop_order=3, cumulative_time=25),
        dict(route_name="DJ", stop_name="dormitory_o", stop_order=0, cumulative_time=-5),
        dict(route_name="DJ", stop_name="shuttlecock_o", stop_order=1, cumulative_time=0),
        dict(route_name="DJ", stop_name="station", stop_order=2, cumulative_time=10),
        dict(route_name="DJ", stop_name="jungang_stn", stop_order=3, cumulative_time=13),
        dict(route_name="DJ", stop_name="shuttlecock_i", stop_order=4, cumulative_time=20),
        dict(route_name="DJ", stop_name="dormitory_i", stop_order=5, cumulative_time=25),
    ]
    insert_statement = insert(ShuttleRouteStop).values(route_stop_list)
    insert_statement = insert_statement.on_conflict_do_update(
        constraint="pk_shuttle_route_stop",
        set_=dict(
            stop_order=insert_statement.excluded.stop_order,
            cumulative_time=insert_statement.excluded.cumulative_time,
        ),
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
                    shuttle_type = f"{shuttle_type}C"
                    shuttle_start_stop = "shuttlecock_o"
                elif shuttle_start_stop == "Dormitory":
                    shuttle_start_stop = "dormitory_o"
                timetable.append(
                    dict(
                        route_name=shuttle_type,
                        period_type=period,
                        weekday=day_dict[day] == "weekdays",
                        start_stop=shuttle_start_stop,
                        departure_time=f"{shuttle_time}:00+09:00",
                    ),
                )
    insert_statement = insert(ShuttleTimetable).values(timetable)
    insert_statement = insert_statement.on_conflict_do_update(
        constraint="pk_shuttle_timetable",
        set_=dict(start_stop=insert_statement.excluded.start_stop),
    )
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_commute_shuttle_route(db_session: Session):
    route_list = [
        dict(route_name="1",
             route_description_korean="화정/백석/마두/대화",
             route_description_english="Hwajeong/Baeksuk/Madu/Daehwa"),
        dict(route_name="2",
             route_description_korean="공항/목동/신정/광명",
             route_description_english="Gimpo Airport/Mokdong/Sinjeong/Gwangmyeong"),
        dict(route_name="3",
             route_description_korean="상도/봉천/신림/시흥",
             route_description_english="Sangdo/Bongcheon/Sinlim/Siheung"),
        dict(route_name="4",
             route_description_korean="천호/잠실/성남/수내",
             route_description_english="Cheonho/Jamsil/Sungnam/Sunae"),
        dict(route_name="5",
             route_description_korean="정자/죽전/수지/광교",
             route_description_english="Jeongja/Jukjeon/Suji/Gwanggyo"),
        dict(route_name="A",
             route_description_korean="화정/백석/마두/대화",
             route_description_english="Hwajeong/Baeksuk/Madu/Daehwa"),
        dict(route_name="B",
             route_description_korean="광명/구로/여의도",
             route_description_english="Gwangmyeong/Guro/Yeouido"),
        dict(route_name="C",
             route_description_korean="복정/송파/잠실/천호",
             route_description_english="Bokjeong/Songpa/Jamsil/Cheonho"),
        dict(route_name="D",
             route_description_korean="수지/죽전/정자/야탑",
             route_description_english="Suji/Jukjeon/Jeongja/Yatap"),
    ]
    insert_statement = insert(CommuteShuttleRoute).values(route_list)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["route_name"],
        set_=dict(
            route_description_korean=insert_statement.excluded.route_description_korean,
            route_description_english=insert_statement.excluded.route_description_english,
        ),
    )
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_commute_shuttle_stop(db_session: Session):
    base_url = "https://raw.githubusercontent.com/hyuabot-developers/hyuabot-shuttle-timetable/main"
    url = f"{base_url}/commute/stop.csv"
    stop_list: list[dict] = []
    async with ClientSession() as session:
        async with session.get(url) as response:
            reader = csv.reader((await response.text()).splitlines(), delimiter=",")
            for stop_name, description, latitude, longitude in reader:
                stop_list.append(dict(
                    stop_name=stop_name, description=description,
                    latitude=latitude, longitude=longitude))
    insert_statement = insert(CommuteShuttleStop).values(stop_list)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["stop_name"],
        set_=dict(
            description=insert_statement.excluded.description,
            latitude=insert_statement.excluded.latitude,
            longitude=insert_statement.excluded.longitude,
        ),
    )
    db_session.execute(insert_statement)
    db_session.commit()


async def insert_commute_shuttle_timetable(db_session: Session):
    base_url = "https://raw.githubusercontent.com/hyuabot-developers/hyuabot-shuttle-timetable/main"
    url = f"{base_url}/commute/route.csv"
    timetable_list: list[dict] = []
    stop_index_dict: defaultdict[str, int] = defaultdict(int)
    async with ClientSession() as session:
        async with session.get(url) as response:
            reader = csv.reader((await response.text()).splitlines(), delimiter=",")
            for route_name, stop_name, departure_time in reader:
                timetable_list.append(dict(
                    route_name=route_name, stop_order=stop_index_dict[route_name],
                    stop_name=stop_name, departure_time=f"{departure_time}+09:00"))
                stop_index_dict[route_name] += 1
    insert_statement = insert(CommuteShuttleTimetable).values(timetable_list)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["route_name", "stop_name"],
        set_=dict(
            stop_order=insert_statement.excluded.stop_order,
            departure_time=insert_statement.excluded.departure_time,
        ),
    )
    db_session.execute(insert_statement)
    db_session.commit()
