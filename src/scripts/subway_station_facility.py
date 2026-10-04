import csv
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.subway_station_facility import SubwayStationFacility


CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "subway_station_facility.csv"
FIELDS = (
    "station_id",
    "facility_type",
    "sort_order",
    "exit_no",
    "from_place",
    "to_place",
    "description_korean",
    "description_english",
    "source",
)


def parse_subway_station_facilities(path: Path = CSV_PATH) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as csv_file:
        rows = csv.DictReader(csv_file)
        if tuple(rows.fieldnames or ()) != FIELDS:
            raise ValueError(f"Unexpected subway station facility CSV columns: {rows.fieldnames}")
        result = []
        for row in rows:
            row["sort_order"] = int(row["sort_order"] or 0)
            row["source"] = row["source"] or "KR_NETWORK"
            result.append(row)
        return result


async def insert_subway_station_facilities(db_session: Session):
    facilities = parse_subway_station_facilities()
    if not facilities:
        return
    statement = insert(SubwayStationFacility).values(facilities)
    statement = statement.on_conflict_do_update(
        index_elements=["station_id", "facility_type", "sort_order"],
        set_={
            column: getattr(statement.excluded, column)
            for column in FIELDS
            if column not in {"station_id", "facility_type", "sort_order"}
        },
    )
    db_session.execute(statement)
    db_session.commit()
