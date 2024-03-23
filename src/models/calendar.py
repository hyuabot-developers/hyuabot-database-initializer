import datetime

from sqlalchemy import DateTime, String, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped

from models import BaseModel


class CalendarVersion(BaseModel):
    __tablename__ = "academic_calendar_version"
    version_id: Mapped[int] = mapped_column(primary_key=True)
    version_name: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class CalendarCategory(BaseModel):
    __tablename__ = "academic_calendar_category"
    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(30), nullable=False)


class Calendar(BaseModel):
    __tablename__ = "academic_calendar"
    __table_args__ = (
        ForeignKeyConstraint(["category_id"], ["academic_calendar_category.category_id"]),
    )
    academic_calendar_id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(nullable=False)
