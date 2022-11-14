from aiohttp import ClientSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.reading_room import ReadingRoom


async def insert_reading_room_data(db_session: Session):
    url = "https://lib.hanyang.ac.kr/smufu-api/pc/0/rooms-at-seat"
    room_list: list[dict] = []
    async with ClientSession() as session:
        async with session.get(url) as response:
            json_body = await response.json()
            for room in json_body["data"]["list"]:
                room_list.append(
                    dict(
                        room_id=room["id"],
                        room_name=room["name"],
                        campus_id=room["branchGroup"]["id"],
                        is_active=room["isActive"],
                        is_reservable=room["isReservable"],
                        total_seat_count=room["total"],
                        total_active_seat_count=room["activeTotal"],
                        occupied_seat_count=room["occupied"],
                        available_seat_count=room["available"],
                    )
                )
    insert_statement = insert(ReadingRoom).values(room_list)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["room_id"],
        set_=dict(
            room_name=insert_statement.excluded.room_name,
            campus_id=insert_statement.excluded.campus_id,
            is_active=insert_statement.excluded.is_active,
            is_reservable=insert_statement.excluded.is_reservable,
            total_seat_count=insert_statement.excluded.total_seat_count,
            total_active_seat_count=insert_statement.excluded.total_active_seat_count,
            occupied_seat_count=insert_statement.excluded.occupied_seat_count,
            available_seat_count=insert_statement.excluded.available_seat_count,
        ),
    )
    db_session.execute(insert_statement)
    db_session.commit()
