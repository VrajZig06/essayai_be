from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EssaySubmission(BaseModel):
    essay_text: str = Field(..., min_length=100, description="Essay text content (minimum 100 characters)")
    title: Optional[str] = Field(None, max_length=200, description="Optional essay title")

class EssayEvaluationResult(BaseModel):
    clarity_of_thoughts_score: int
    clarity_of_thoughts_feedback: str
    language_quality_score: int
    language_quality_feedback: str
    depth_analysis_score: int
    depth_analysis_feedback: str
    overall_score: int
    overall_feedback: str

class EssayResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    essay_text: str
    clarity_of_thoughts_score: int
    clarity_of_thoughts_feedback: str
    language_quality_score: int
    language_quality_feedback: str
    depth_analysis_score: int
    depth_analysis_feedback: str
    overall_score: int
    overall_feedback: str
    created_at: Optional[str]
    updated_at: Optional[str]

class EssayHistoryResponse(BaseModel):
    essays: List[EssayResponse]
    total_essays: int

class UserDashboardStats(BaseModel):
    total_essays: int
    average_score: float
    highest_score: int
    lowest_score: int
    total_clarity_score: int
    total_language_score: int
    total_depth_score: int
    recent_essays: List[EssayResponse]

class PerformanceLevel(BaseModel):
    level: str
    count: int
    percentage: float

class PerformanceBreakdown(BaseModel):
    exceptional: PerformanceLevel
    excellent: PerformanceLevel
    good: PerformanceLevel
    needs_improvement: PerformanceLevel
    poor: PerformanceLevel
