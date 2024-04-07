import asyncio

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup, Tag
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.bus import BusStop, BusRoute, BusRouteStop


async def insert_bus_stop(db_session: Session):
    keywords = ["경기테크노파크", "한양대", "한국생산기술연구원", "성안길입구", "신안산대학교",
                "새솔고", "상록수역", "수원역", "강남역우리은행", "본오동", "한라비발디1차",
                "푸르지오6차후문", "선부동차고지", "안산역", "경인합섬앞", "오목천차고지",
                "안산해솔초등학교", "그랑시티자이", "광명역", "파크푸르지오", "성포주공",
                "한국생산기술연구원",
                "원시역", "시우역", "강남역", "파이낸셜뉴스"]
    tasks = [fetch_bus_stop(db_session, keyword) for keyword in keywords]
    await asyncio.gather(*tasks)
    db_session.commit()


async def fetch_bus_stop(db_session: Session, keyword: str):
    url = "http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=" \
          f"1234567890&keyword={keyword}"
    stop_list: list[dict] = []
    timeout = ClientTimeout(total=30.0)
    try:
        async with ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), features="xml")
                response_item = soup.find("response")
                if response_item is None:
                    return
                message_body = response_item.find("msgBody")
                if not isinstance(message_body, Tag):
                    return
                station_list = message_body.find_all("busStationList")
                for station in station_list:
                    stop_list.append(dict(
                        stop_id=station.find("stationId").text,
                        stop_name=station.find("stationName").text,
                        district_code=station.find("districtCd").text,
                        mobile_number=str(station.find("mobileNo").text).strip(),
                        region_name=station.find("regionName").text,
                        latitude=station.find("x").text,
                        longitude=station.find("y").text,
                    ))
                insert_statement = insert(BusStop).values(stop_list)
                insert_statement = insert_statement.on_conflict_do_update(
                    index_elements=["stop_id"],
                    set_=dict(
                        stop_name=insert_statement.excluded.stop_name,
                        district_code=insert_statement.excluded.district_code,
                        mobile_number=insert_statement.excluded.mobile_number,
                        region_name=insert_statement.excluded.region_name,
                        latitude=insert_statement.excluded.latitude,
                        longitude=insert_statement.excluded.longitude,
                    ),
                )
                db_session.execute(insert_statement)
                db_session.commit()
    except asyncio.exceptions.TimeoutError:
        print("TimeoutError", url)
    except AttributeError:
        print("AttributeError", url)


async def insert_bus_route(db_session: Session):
    routes = [
        "10-1", "62", "3100", "3100N", "3101", "3102", "110", "707", "7070",
        "707-1", "9090", "50"]
    tasks = [fetch_bus_route_list(db_session, route) for route in routes]
    await asyncio.gather(*tasks)
    db_session.commit()


async def fetch_bus_route_list(db_session: Session, keyword: str):
    url = f"http://openapi.gbis.go.kr/ws/rest/busrouteservice?serviceKey=1234567890&keyword={keyword}"
    route_list: list[str] = []
    timeout = ClientTimeout(total=30.0)
    try:
        async with ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), features="xml")
                response_item = soup.find("response")
                if response_item is None:
                    return
                message_body = response_item.find("msgBody")
                if not isinstance(message_body, Tag):
                    return
                route_search_list = message_body.find_all("busRouteList")
                for route in route_search_list:
                    if "안산" in route.find("regionName").text and keyword == route.find("routeName").text:
                        route_list.append(route.find("routeId").text)
                tasks = [insert_bus_route_item(db_session, route_id) for route_id in route_list]
                await asyncio.gather(*tasks)
    except asyncio.exceptions.TimeoutError:
        print("TimeoutError", url)
    except AttributeError:
        print("AttributeError", url)


async def insert_bus_route_item(db_session: Session, route_id: str):
    url = f"http://openapi.gbis.go.kr/ws/rest/busrouteservice/info" \
          f"?serviceKey=1234567890&routeId={route_id}"
    route_list: list[dict] = []
    timeout = ClientTimeout(total=30.0)
    try:
        async with ClientSession(timeout=timeout, trust_env=True) as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), features="xml")
                response_item = soup.find("response")
                if response_item is None:
                    return
                message_body = response_item.find("msgBody")
                if not isinstance(message_body, Tag):
                    return
                route_search_result = message_body.find_all("busRouteInfoItem")
                if len(route_search_result) == 0:
                    return
                route_search_item = route_search_result[0]
                route_list.append(dict(
                    company_id=route_search_item.find("companyId").text,
                    company_name=route_search_item.find("companyName").text,
                    company_telephone=route_search_item.find("companyTel").text,
                    district_code=route_search_item.find("districtCd").text,
                    up_first_time=f"{route_search_item.find('upFirstTime').text} +09:00",
                    up_last_time=f"{route_search_item.find('upLastTime').text} +09:00",
                    down_first_time=f"{route_search_item.find('downFirstTime').text} +09:00",
                    down_last_time=f"{route_search_item.find('downLastTime').text} +09:00",
                    start_stop_id=route_search_item.find("startStationId").text,
                    end_stop_id=route_search_item.find("endStationId").text,
                    route_id=route_search_item.find("routeId").text,
                    route_name=route_search_item.find("routeName").text,
                    route_type_code=route_search_item.find("routeTypeCd").text,
                    route_type_name=route_search_item.find("routeTypeName").text,
                ))
                insert_statement = insert(BusRoute).values(route_list)
                insert_statement = insert_statement.on_conflict_do_update(
                    index_elements=["route_id"],
                    set_=dict(
                        company_id=insert_statement.excluded.company_id,
                        company_name=insert_statement.excluded.company_name,
                        company_telephone=insert_statement.excluded.company_telephone,
                        district_code=insert_statement.excluded.district_code,
                        up_first_time=insert_statement.excluded.up_first_time,
                        up_last_time=insert_statement.excluded.up_last_time,
                        down_first_time=insert_statement.excluded.down_first_time,
                        down_last_time=insert_statement.excluded.down_last_time,
                        start_stop_id=insert_statement.excluded.start_stop_id,
                        end_stop_id=insert_statement.excluded.end_stop_id,
                        route_name=insert_statement.excluded.route_name,
                        route_type_code=insert_statement.excluded.route_type_code,
                        route_type_name=insert_statement.excluded.route_type_name,
                    ),
                )
                db_session.execute(insert_statement)
                db_session.commit()
    except asyncio.exceptions.TimeoutError:
        print("TimeoutError", url)
    except AttributeError:
        print("AttributeError", url)


async def insert_bus_route_stop(db_session: Session):
    bus_route_stop_list = [
        dict(route_id="216000026", stop_id="216000719", stop_sequence=10, start_stop_id=217000283),  # 3100(한양대정문)
        dict(route_id="216000096", stop_id="216000719", stop_sequence=10, start_stop_id=217000283),  # 3100N(한양대정문)
        dict(route_id="216000043", stop_id="216000719", stop_sequence=10, start_stop_id=217000283),  # 3101(한양대정문)
        dict(route_id="216000070", stop_id="216000719", stop_sequence=10, start_stop_id=217000283),  # 707-1(한양대정문)
        dict(route_id="216000061", stop_id="216000383", stop_sequence=17, start_stop_id=233003145),  # 3102(한양대기숙사앞)
        dict(route_id="216000061", stop_id="216000381", stop_sequence=18, start_stop_id=233003145),  # 3102(한국생산기술연구원)
        dict(route_id="216000061", stop_id="216000379", stop_sequence=19, start_stop_id=233003145),  # 3102(ERICA컨벤션센터)
        dict(route_id="216000068", stop_id="216000383", stop_sequence=12, start_stop_id=216000020),  # 10-1(한양대기숙사앞)
        dict(route_id="216000068", stop_id="216000381", stop_sequence=13, start_stop_id=216000020),  # 10-1(한국생산기술연구원)
        dict(route_id="216000068", stop_id="216000379", stop_sequence=14, start_stop_id=216000020),  # 10-1(ERICA컨벤션센터)
        dict(route_id="216000068", stop_id="216000138", stop_sequence=21, start_stop_id=216000145),  # 10-1(상록수역3번출구)
        dict(route_id="216000016", stop_id="216000152", stop_sequence=16, start_stop_id=216000053),  # 62(성안길입구)
        dict(route_id="217000014", stop_id="216000070", stop_sequence=31, start_stop_id=217000066),  # 110(한양대입구)
        dict(route_id="216000104", stop_id="216000070", stop_sequence=20, start_stop_id=217000293),  # 7070(한양대입구)
        dict(route_id="200000015", stop_id="216000070", stop_sequence=50, start_stop_id=217000626),  # 909(한양대입구)
        dict(route_id="216000075", stop_id="216000759", stop_sequence=15, start_stop_id=216000358),  # 50(안산파크푸르지오)
        dict(route_id="216000075", stop_id="216000117", stop_sequence=78, start_stop_id=213000487),  # 50(성포주공4단지)
    ]
    insert_statement = insert(BusRouteStop).values(bus_route_stop_list)
    insert_statement = insert_statement.on_conflict_do_update(
        constraint="pk_bus_route_stop",
        set_=dict(stop_sequence=insert_statement.excluded.stop_sequence),
    )
    db_session.execute(insert_statement)
    db_session.commit()
