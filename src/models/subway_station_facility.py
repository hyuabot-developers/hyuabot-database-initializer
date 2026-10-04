from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.shuttle import BaseModel


class SubwayStationFacility(BaseModel):
    __tablename__ = "subway_station_facility"
    __table_args__ = (
        UniqueConstraint("station_id", "facility_type", "sort_order", name="idx_subway_station_facility"),
    )

    seq: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    station_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("subway_route_station.station_id"), nullable=False
    )
    facility_type: Mapped[str] = mapped_column(String(20), nullable=False)
    sort_order: Mapped[int] = mapped_column(nullable=False, default=0)
    exit_no: Mapped[str | None] = mapped_column(String(10))
    from_place: Mapped[str | None] = mapped_column(String(50))
    to_place: Mapped[str | None] = mapped_column(String(50))
    description_korean: Mapped[str | None] = mapped_column(String(200))
    description_english: Mapped[str | None] = mapped_column(String(200))
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="KR_NETWORK")
