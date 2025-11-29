import pytz
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.models import BaseModel


if TYPE_CHECKING:
    from app.infrastructure.db.models import UserModel


class AccountModel(BaseModel):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True ,index=True)
    email: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=text("TIMEZONE('Europe/Moscow', NOW())"))

    users: Mapped[List["UserModel"]] = relationship("UserModel", back_populates="account")
