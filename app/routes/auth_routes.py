from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session
from app.schema.user_schema import (
    LoginRequest, LoginResponse, ForgotPasswordRequest, 
    ResetPasswordRequest, EmailVerificationRequest, ChangePasswordRequest
)
from app.services.user_service import UserService
from app.db.session import get_db
from app.utils.response import error_response
from app.utils.messages import ErrorMessages
from app.utils.jwt import validate_token

router = APIRouter()

def get_current_user(token: str = Depends(validate_token), db: Session = Depends(get_db)):
    """Dependency to get current authenticated user"""
    try:
        user_id = token.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_service = UserService(db)
        user = user_service.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    except Exception:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication"
        )

@router.post("/login", response_model=LoginResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    """Login user with email and password"""
    try:
        user_service = UserService(db)
        return user_service.user_login(data)
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

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send password reset link to user's email"""
    try:
        user_service = UserService(db)
        return user_service.forgot_password(data)
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

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset user password using reset token"""
    try:
        user_service = UserService(db)
        return user_service.reset_password(data)
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

@router.post("/verify-email")
def verify_email(data: EmailVerificationRequest, db: Session = Depends(get_db)):
    """Verify user email using verification token"""
    try:
        user_service = UserService(db)
        return user_service.verify_email(data)
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

@router.get("/verify-email")
def verify_email_get(token: str, db: Session = Depends(get_db)):
    """Verify user email using verification token (GET method for email links)"""
    try:
        verification_data = EmailVerificationRequest(token=token)
        user_service = UserService(db)
        return user_service.verify_email(verification_data)
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

@router.get("/reset-password")
def reset_password_get(token: str, db: Session = Depends(get_db)):
    """Get reset password form (GET method for email links)"""
    return {
        "message": "Please use POST /reset-password with your token and new password",
        "token": token
    }

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password (requires authentication)"""
    try:
        user_service = UserService(db)
        return user_service.change_password(current_user.id, data)
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
