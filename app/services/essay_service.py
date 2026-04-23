from app.repositories.essay_repo import EssayRepo
from app.utils.messages import ErrorMessages, SuccessMessages
from sqlalchemy.orm import Session
from fastapi import HTTPException, status as http_status
from app.schema.essay_schema import (
    EssaySubmission, EssayResponse, EssayHistoryResponse, 
    UserDashboardStats, PerformanceBreakdown
)
from app.utils.response import success_response
from typing import List
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from llm import workflow, EssayState

class EssayService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.essay_repo = EssayRepo(db)

    def submit_essay(self, user_id: str, essay_data: EssaySubmission):
        """Submit essay for evaluation"""
        try:
            # Evaluate essay using AI
            evaluation_result = self._evaluate_essay(essay_data.essay_text)
            
            # Create essay record with evaluation results
            essay_record_data = {
                'user_id': user_id,
                'title': essay_data.title,
                'essay': essay_data.essay_text,
                'clarity_of_thoughts_score': evaluation_result['clarity_of_thoughts_score'],
                'clarity_of_thoughts_feedback': evaluation_result['clarity_of_thoughts_feedback'],
                'language_quality_score': evaluation_result['language_quality_score'],
                'language_quality_feedback': evaluation_result['language_quality_feedback'],
                'depth_analysis_score': evaluation_result['depth_analysis_score'],
                'depth_analysis_feedback': evaluation_result['depth_analysis_feedback'],
                'overall_score': evaluation_result['final_score'],
                'overall_feedback': evaluation_result['final_feedback']
            }
            
            # Save to database
            essay_record = self.essay_repo.create_essay(essay_record_data)
            
            # Helper function to handle datetime conversion
            def format_datetime(dt):
                if dt is None:
                    return None
                # Check if it's already a datetime object
                if hasattr(dt, 'isoformat'):
                    return dt.isoformat()
                # If it's a timestamp (integer), convert to datetime first
                elif isinstance(dt, (int, float)):
                    from datetime import datetime
                    return datetime.fromtimestamp(dt / 1000 if dt > 1e10 else dt).isoformat()
                # If it's already a string, return as is
                elif isinstance(dt, str):
                    return dt
                else:
                    return str(dt)
            
            # Format response directly from the created record
            response_data = EssayResponse(
                id=str(essay_record.id),
                user_id=essay_record.user_id,
                title=essay_record.title,
                essay_text=essay_record.essay,
                clarity_of_thoughts_score=essay_record.clarity_of_thoughts_score,
                clarity_of_thoughts_feedback=essay_record.clarity_of_thoughts_feedback,
                language_quality_score=essay_record.language_quality_score,
                language_quality_feedback=essay_record.language_quality_feedback,
                depth_analysis_score=essay_record.depth_analysis_score,
                depth_analysis_feedback=essay_record.depth_analysis_feedback,
                overall_score=essay_record.overall_score,
                overall_feedback=essay_record.overall_feedback,
                created_at=format_datetime(essay_record.created_at),
                updated_at=format_datetime(essay_record.updated_at)
            )
            
            return success_response(
                message=SuccessMessages.ESSAY_SUBMITTED_SUCCESSFULLY,
                status_code=http_status.HTTP_201_CREATED,
                data=response_data
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing essay: {str(e)}"
            )

    def get_user_essays(self, user_id: str, limit: int = 50, offset: int = 0):
        """Get user's essay history"""
        try:
            essays = self.essay_repo.get_by_user_id(user_id, limit, offset)
            total_essays = self.essay_repo.count_user_essays(user_id)
            
            essay_responses = [self._format_essay_response(essay) for essay in essays]
            
            return success_response(
                data=EssayHistoryResponse(
                    essays=essay_responses,
                    total_essays=total_essays
                )
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching essay history: {str(e)}"
            )

    def get_user_dashboard(self, user_id: str):
        """Get user dashboard with statistics and recent essays"""
        try:
            # Get user statistics
            stats = self.essay_repo.get_user_stats(user_id)
            performance_breakdown = self.essay_repo.get_performance_breakdown(user_id)
            
            # Get recent essays (last 5)
            recent_essays = self.essay_repo.get_by_user_id(user_id, limit=5, offset=0)
            recent_essay_responses = [self._format_essay_response(essay) for essay in recent_essays]
            
            dashboard_data = UserDashboardStats(
                total_essays=stats['total_essays'],
                average_score=stats['average_score'],
                highest_score=stats['highest_score'],
                lowest_score=stats['lowest_score'],
                total_clarity_score=stats['total_clarity_score'],
                total_language_score=stats['total_language_score'],
                total_depth_score=stats['total_depth_score'],
                recent_essays=recent_essay_responses
            )
            
            return success_response(
                data={
                    'stats': dashboard_data,
                    'performance_breakdown': performance_breakdown
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching dashboard data: {str(e)}"
            )

    def _evaluate_essay(self, essay_text: str) -> dict:
        """Evaluate essay using AI workflow"""
        try:
            # Run the AI evaluation workflow
            result = workflow.invoke({"essay": essay_text})
            
            return {
                'clarity_of_thoughts_score': result.get('clarity_of_thoughts_score', 0),
                'clarity_of_thoughts_feedback': result.get('clarity_of_thoughts_feedback', ''),
                'language_quality_score': result.get('language_quality_score', 0),
                'language_quality_feedback': result.get('language_quality_feedback', ''),
                'depth_analysis_score': result.get('depth_analysis_score', 0),
                'depth_analysis_feedback': result.get('depth_analysis_feedback', ''),
                'final_score': result.get('final_score', 0),
                'final_feedback': result.get('final_feedback', '')
            }
        except Exception as e:
            # Fallback to default values if AI evaluation fails
            print(f"AI Evaluation Error: {str(e)}")
            return {
                'clarity_of_thoughts_score': 5,
                'clarity_of_thoughts_feedback': 'Unable to evaluate clarity at this time.',
                'language_quality_score': 5,
                'language_quality_feedback': 'Unable to evaluate language quality at this time.',
                'depth_analysis_score': 5,
                'depth_analysis_feedback': 'Unable to evaluate depth analysis at this time.',
                'final_score': 15,
                'final_feedback': 'Essay evaluation system is currently experiencing issues. Please try again later.'
            }

    def _format_essay_response(self, essay_record) -> EssayResponse:
        """Format essay record for API response"""
        # Helper function to handle datetime conversion
        def format_datetime(dt):
            if dt is None:
                return None
            # Check if it's already a datetime object
            if hasattr(dt, 'isoformat'):
                return dt.isoformat()
            # If it's a timestamp (integer), convert to datetime first
            elif isinstance(dt, (int, float)):
                from datetime import datetime
                return datetime.fromtimestamp(dt / 1000 if dt > 1e10 else dt).isoformat()
            # If it's already a string, return as is
            elif isinstance(dt, str):
                return dt
            else:
                return str(dt)
        
        return EssayResponse(
            id=str(essay_record.id),
            user_id=essay_record.user_id,
            title=essay_record.title,
            essay_text=essay_record.essay,
            clarity_of_thoughts_score=essay_record.clarity_of_thoughts_score,
            clarity_of_thoughts_feedback=essay_record.clarity_of_thoughts_feedback,
            language_quality_score=essay_record.language_quality_score,
            language_quality_feedback=essay_record.language_quality_feedback,
            depth_analysis_score=essay_record.depth_analysis_score,
            depth_analysis_feedback=essay_record.depth_analysis_feedback,
            overall_score=essay_record.overall_score,
            overall_feedback=essay_record.overall_feedback,
            created_at=format_datetime(essay_record.created_at),
            updated_at=format_datetime(essay_record.updated_at)
        )
