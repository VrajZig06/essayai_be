from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Text
from app.db.models.base import Base, TimestampMixin

class EssayResults(Base, TimestampMixin):

    __tablename__ = "essays"

    user_id: Mapped[str] = mapped_column(String(40), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    essay: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Clarity of Thoughts
    clarity_of_thoughts_feedback: Mapped[str] = mapped_column(Text, nullable=False)
    clarity_of_thoughts_score: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Language Quality
    language_quality_feedback: Mapped[str] = mapped_column(Text, nullable=False)
    language_quality_score: Mapped[int] = mapped_column(Integer, nullable=False)

    # Depth of analysis
    depth_analysis_feedback: Mapped[str] = mapped_column(Text, nullable=False)
    depth_analysis_score: Mapped[int] = mapped_column(Integer, nullable=False)

    # Overall 
    overall_feedback: Mapped[str] = mapped_column(Text, nullable=False)
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)