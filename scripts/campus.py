from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.campus import Campus


async def insert_campus_data(db_session: Session):
    supported_campuses = [
        dict(campus_id=1, campus_name="서울"),
        dict(campus_id=2, campus_name="ERICA"),
    ]
    insert_statement = insert(Campus).values(supported_campuses)
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["campus_id"],
        set_=dict(campus_name=insert_statement.excluded.campus_name),
    )
    db_session.execute(insert_statement)
    db_session.commit()
