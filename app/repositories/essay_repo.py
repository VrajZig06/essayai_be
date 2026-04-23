from app.repositories.base_repo import BaseRepository
from app.db.models.essay_model import EssayResults
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc, func

class EssayRepo(BaseRepository[EssayResults]):
    """Repository for Essay model operations."""
    
    def __init__(self, db: Session):
        """
        Initialize Essay repository.

        Args:
            db: Database session
        """
        super().__init__(EssayResults, db)
    
    def get_by_user_id(self, user_id: str, limit: int = 50, offset: int = 0) -> List[EssayResults]:
        """
        Get essays by user ID with pagination.

        Args:
            user_id: User's ID
            limit: Number of essays to return
            offset: Number of essays to skip

        Returns:
            List of essays for the user
        """
        return (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.is_deleted == False)
            .order_by(desc(EssayResults.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    def count_user_essays(self, user_id: str) -> int:
        """
        Count total essays for a user.

        Args:
            user_id: User's ID

        Returns:
            Total number of essays for the user
        """
        return (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.is_deleted == False)
            .count()
        )
    
    def get_user_stats(self, user_id: str) -> dict:
        """
        Get statistics for a user's essays.

        Args:
            user_id: User's ID

        Returns:
            Dictionary with user statistics
        """
        stats = (
            self.db.query(
                func.count(EssayResults.id).label('total_essays'),
                func.avg(EssayResults.overall_score).label('average_score'),
                func.max(EssayResults.overall_score).label('highest_score'),
                func.min(EssayResults.overall_score).label('lowest_score'),
                func.sum(EssayResults.clarity_of_thoughts_score).label('total_clarity_score'),
                func.sum(EssayResults.language_quality_score).label('total_language_score'),
                func.sum(EssayResults.depth_analysis_score).label('total_depth_score')
            )
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.is_deleted == False)
            .first()
        )
        
        return {
            'total_essays': stats.total_essays or 0,
            'average_score': float(stats.average_score or 0),
            'highest_score': stats.highest_score or 0,
            'lowest_score': stats.lowest_score or 0,
            'total_clarity_score': stats.total_clarity_score or 0,
            'total_language_score': stats.total_language_score or 0,
            'total_depth_score': stats.total_depth_score or 0
        }
    
    def get_performance_breakdown(self, user_id: str) -> dict:
        """
        Get performance breakdown for a user.

        Args:
            user_id: User's ID

        Returns:
            Dictionary with performance breakdown by level
        """
        total_essays = self.count_user_essays(user_id)
        if total_essays == 0:
            return {
                'exceptional': {'count': 0, 'percentage': 0},
                'excellent': {'count': 0, 'percentage': 0},
                'good': {'count': 0, 'percentage': 0},
                'needs_improvement': {'count': 0, 'percentage': 0},
                'poor': {'count': 0, 'percentage': 0}
            }
        
        exceptional = (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.overall_score >= 27)
            .filter(EssayResults.is_deleted == False)
            .count()
        )
        
        excellent = (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.overall_score >= 21)
            .filter(EssayResults.overall_score < 27)
            .filter(EssayResults.is_deleted == False)
            .count()
        )
        
        good = (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.overall_score >= 15)
            .filter(EssayResults.overall_score < 21)
            .filter(EssayResults.is_deleted == False)
            .count()
        )
        
        needs_improvement = (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.overall_score >= 9)
            .filter(EssayResults.overall_score < 15)
            .filter(EssayResults.is_deleted == False)
            .count()
        )
        
        poor = (
            self.db.query(EssayResults)
            .filter(EssayResults.user_id == user_id)
            .filter(EssayResults.overall_score < 9)
            .filter(EssayResults.is_deleted == False)
            .count()
        )
        
        return {
            'exceptional': {
                'count': exceptional,
                'percentage': round((exceptional / total_essays) * 100, 2)
            },
            'excellent': {
                'count': excellent,
                'percentage': round((excellent / total_essays) * 100, 2)
            },
            'good': {
                'count': good,
                'percentage': round((good / total_essays) * 100, 2)
            },
            'needs_improvement': {
                'count': needs_improvement,
                'percentage': round((needs_improvement / total_essays) * 100, 2)
            },
            'poor': {
                'count': poor,
                'percentage': round((poor / total_essays) * 100, 2)
            }
        }
    
    def create_essay(self, essay_data: dict) -> EssayResults:
        """
        Create a new essay record.

        Args:
            essay_data: Dictionary with essay data

        Returns:
            Created essay record
        """
        new_essay = EssayResults(**essay_data)
        self.db.add(new_essay)
        self.db.commit()
        self.db.refresh(new_essay)
        return new_essay
