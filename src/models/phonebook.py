import datetime

from sqlalchemy import String, ForeignKeyConstraint, DateTime, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class PhoneBookVersion(BaseModel):
    __tablename__ = "phonebook_version"
    version_id: Mapped[int] = mapped_column(primary_key=True)
    version_name: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)


class PhoneBookCategory(BaseModel):
    __tablename__ = "phonebook_category"
    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(30), nullable=False)


class PhoneBook(BaseModel):
    __tablename__ = "phonebook"
    __table_args__ = (
        ForeignKeyConstraint(["campus_id"], ["campus.campus_id"]),
        ForeignKeyConstraint(["category_id"], ["phonebook_category.category_id"]),
    )
    phonebook_id: Mapped[int] = mapped_column(primary_key=True)
    campus_id: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
