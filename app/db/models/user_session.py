from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, null
from app.db.models.base import Base, TimestampMixin

class UserSession(Base, TimestampMixin):

    __tablename__ = "user_sessions"

    user_id: Mapped[str] = mapped_column(String(40), ForeignKey("users.id"), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255),nullable=True, default=None)
    