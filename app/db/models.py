from sqlalchemy import (
    Integer,
    String,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import datetime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    signup_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
