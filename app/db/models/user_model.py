from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Column, Integer, Float, String, null
from app.db.models.base import Base, TimestampMixin
from enum import Enum

class AccountType(Enum):
    P = "p"  # phone
    E = "e"  # email

class User(Base, TimestampMixin):

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False) 
    email: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    phone: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[AccountType] = mapped_column(String, default=AccountType.E)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    otp: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    email_verification_token: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    password_reset_token: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    password_reset_expires: Mapped[Integer] = mapped_column(Integer, nullable=True, default=None)