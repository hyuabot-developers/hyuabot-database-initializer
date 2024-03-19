from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.restaurant import Restaurant


async def insert_restaurant_data(db_session: Session):
    supported_restaurants = [
        dict(
            restaurant_id=1, restaurant_name="학생식당", campus_id=1, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="10:30~15:00/10:00~14:00(토요일)/마감 14:50",
            dinner_time="16:00~18:30/마감 18:20",
        ),
        dict(
            restaurant_id=2, restaurant_name="생활과학관식당", campus_id=1, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="11:30~14:00/11:30~13:30(토요일)",
            dinner_time="17:00~18:30",
        ),
        dict(
            restaurant_id=4, restaurant_name="신소재공학관 식당", campus_id=1, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="11:30~13:30",
            dinner_time="17:00~18:30",
        ),
        dict(
            restaurant_id=5, restaurant_name="제1생활관 식당", campus_id=1, latitude=0, longitude=0,
            breakfast_time="07:30~09:00",
            lunch_time="12:00~13:30/10:30~13:30 (토요일)",
            dinner_time="17:00~18:20",
        ),
        dict(
            restaurant_id=7, restaurant_name="제2생활관 식당", campus_id=1, latitude=0, longitude=0,
            breakfast_time="07:30~09:00",
            lunch_time="12:00~13:30",
            dinner_time="17:30~18:50",
        ),
        dict(
            restaurant_id=8, restaurant_name="행원파크", campus_id=1, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="11:00~14:00",
            dinner_time=None,
        ),
        dict(
            restaurant_id=11, restaurant_name="교직원식당", campus_id=2, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="11:30~13:30",
            dinner_time=None,
        ),
        dict(
            restaurant_id=12, restaurant_name="학생식당", campus_id=2, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="11:30~13:30",
            dinner_time=None,
        ),
        dict(
            restaurant_id=13, restaurant_name="창의인재원식당", campus_id=2, latitude=0, longitude=0,
            breakfast_time="07:40~09:00",
            lunch_time="11:30~13:20",
            dinner_time="17:10~18:40",
        ),
        dict(
            restaurant_id=14, restaurant_name="푸드코트", campus_id=2, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time=None,
            dinner_time=None,
        ),
        dict(
            restaurant_id=15, restaurant_name="창업보육센터", campus_id=2, latitude=0, longitude=0,
            breakfast_time=None,
            lunch_time="11:30~13:30",
            dinner_time="17:00~18:30",
        ),
    ]
    insert_statement = insert(Restaurant).values(supported_restaurants)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["restaurant_id"],
        set_=dict(
            restaurant_name=insert_statement.excluded.restaurant_name,
            campus_id=insert_statement.excluded.campus_id,
            latitude=insert_statement.excluded.latitude,
            longitude=insert_statement.excluded.longitude,
            breakfast_time=insert_statement.excluded.breakfast_time,
            lunch_time=insert_statement.excluded.lunch_time,
            dinner_time=insert_statement.excluded.dinner_time,
        ),
    )
    db_session.execute(insert_statement)
    db_session.commit()
