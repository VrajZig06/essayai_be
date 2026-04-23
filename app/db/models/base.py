from sqlalchemy import Boolean, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
import time
import uuid
from app.db.base import base

def current_time_ms():
    return int(time.time() * 1000)

class Base(base):
    __abstract__ = True
    
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=lambda: str(uuid.uuid4()))

class TimestampMixin:
    created_at: Mapped[int] = mapped_column(BigInteger, default=current_time_ms)
    updated_at: Mapped[int] = mapped_column(BigInteger,default=current_time_ms,onupdate=current_time_ms)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)