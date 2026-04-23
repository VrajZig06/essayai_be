from fastapi import APIRouter, Depends, HTTPException, status as http_status, Query
from sqlalchemy.orm import Session
from app.schema.essay_schema import EssaySubmission
from app.services.essay_service import EssayService
from app.db.session import get_db
from app.utils.response import error_response
from app.utils.messages import ErrorMessages
from app.utils.jwt import validate_token
from typing import Optional

router = APIRouter()

def get_current_user(db: Session = Depends(get_db), token: dict = Depends(validate_token)):
    """Dependency to get current authenticated user"""
    try:
        user_id = token.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return user_id
    except Exception:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication"
        )

@router.post("/submit")
def submit_essay(
    essay_data: EssaySubmission,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit essay for AI evaluation"""
    try:
        essay_service = EssayService(db)
        return essay_service.submit_essay(current_user_id, essay_data)
    except HTTPException as e:
        return error_response(
            status_code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return error_response(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=ErrorMessages.INTERNAL_SERVER_ERROR.format(e=e)
        )

@router.get("/history")
def get_essay_history(
    limit: int = Query(50, ge=1, le=100, description="Number of essays to return"),
    offset: int = Query(0, ge=0, description="Number of essays to skip"),
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's essay history with pagination"""
    try:
        essay_service = EssayService(db)
        return essay_service.get_user_essays(current_user_id, limit, offset)
    except HTTPException as e:
        return error_response(
            status_code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return error_response(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=ErrorMessages.INTERNAL_SERVER_ERROR.format(e=e)
        )

@router.get("/dashboard")
def get_user_dashboard(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user dashboard with statistics and recent essays"""
    try:
        essay_service = EssayService(db)
        return essay_service.get_user_dashboard(current_user_id)
    except HTTPException as e:
        return error_response(
            status_code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return error_response(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=ErrorMessages.INTERNAL_SERVER_ERROR.format(e=e)
        )
