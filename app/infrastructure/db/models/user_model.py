from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.enums.messenger_type import MessengerType
from app.infrastructure.db.models import BaseModel


if TYPE_CHECKING:
    from app.infrastructure.db.models import AccountModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[str] = mapped_column(String)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    messenger_type: Mapped[MessengerType] =  mapped_column(Enum(MessengerType))
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    account: Mapped["AccountModel"]= relationship("AccountModel", back_populates="users")
