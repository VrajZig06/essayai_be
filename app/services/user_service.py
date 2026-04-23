from app.repositories.user_repo import UserRepo
from app.utils.messages import ErrorMessages, SuccessMessages
from sqlalchemy.orm import Session
from app.utils.hash_text import password_hash, verify_password
from fastapi import HTTPException, status as http_status
from app.schema.user_schema import UserRegistartionResponse, LoginRequest, LoginResponse, ForgotPasswordRequest, ResetPasswordRequest, EmailVerificationRequest, ChangePasswordRequest
from app.utils.response import success_response
from app.utils.template_config import get_template
from app.utils.jwt import generate_token
from app.services.email_service import EmailService
import secrets
import time
from datetime import datetime, timedelta

class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repo = UserRepo(db)

    # User Registraion 
    def user_registration(self, user_data):

        # Validate email and phone for duplication 
        if user_data.get("type") == "e" and self.user_repo.email_exists(user_data.get("email")):

            raise HTTPException(
                status_code = http_status.HTTP_409_CONFLICT,
                detail = ErrorMessages.EMAIL_ALREADY_EXISTS
            )

        elif user_data.get("type") == "p" and self.user_repo.phone_exists(user_data.get("phone")):

            raise HTTPException(
                status_code= http_status.HTTP_409_CONFLICT,
                detail=ErrorMessages.PHONE_NUMBER_ALREADY_EXISTS
            )

        # Extract Password
        password = user_data.get("password")

        # Change simple password to Hashed password
        user_data['password'] = password_hash(password)

        # Now add record to DB
        record = self.user_repo.create(user_data)

        # Send email verification for email-based registration
        if user_data.get("type") == "e" and record.email:
            try:
                email_service = EmailService()
                verification_token = secrets.token_urlsafe(32)
                
                # Update user with verification token
                record.email_verification_token = verification_token
                self.db.commit()
                
                # Send verification email
                email_service.send_email_verification(
                    to_email=record.email,
                    verification_token=verification_token,
                    user_name=f"{record.first_name} {record.last_name}"
                )
            except Exception as e:
                # Log error but don't fail registration
                print(f"Failed to send verification email: {str(e)}")

        return success_response(
            message=SuccessMessages.USER_REGISTRATION_SUCCESSFULLY,
            status_code=http_status.HTTP_201_CREATED,
            data=UserRegistartionResponse.model_validate(record)
        )

    # User Login
    def user_login(self, login_data: LoginRequest):
        user = self.user_repo.get_by_email(login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessages.INVALID_CREDENTIALS
            )
        
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessages.INVALID_CREDENTIALS
            )
        
        # Check if email is verified
        if not user.is_verified:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.EMAIL_NOT_VERIFIED
            )
        
        # Generate JWT token
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        access_token = generate_token(token_data)
        
        return success_response(
            message=SuccessMessages.LOGIN_SUCCESSFULLY,
            data=LoginResponse(
                access_token=access_token,
                user=UserRegistartionResponse.model_validate(user)
            )
        )

    # Forgot Password
    def forgot_password(self, forgot_password_data: ForgotPasswordRequest):
        user = self.user_repo.get_by_email(forgot_password_data.email)
        
        if not user:
            # Don't reveal that email doesn't exist
            return success_response(
                message="If an account with this email exists, a password reset link has been sent."
            )
        
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + 3600  # 1 hour from now
        
        # Update user with reset token
        user.password_reset_token = reset_token
        user.password_reset_expires = expires_at
        self.db.commit()
        
        # Send reset email
        try:
            email_service = EmailService()
            email_service.send_password_reset(
                to_email=user.email,
                reset_token=reset_token,
                user_name=f"{user.first_name} {user.last_name}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send password reset email: {str(e)}"
            )
        
        return success_response(
            message="Password reset link has been sent to your email."
        )

    # Reset Password
    def reset_password(self, reset_password_data: ResetPasswordRequest):
        user = self.user_repo.get_by_field("password_reset_token", reset_password_data.token)
        
        if not user or not user.password_reset_token:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Check if token is expired
        if user.password_reset_expires and int(time.time()) > user.password_reset_expires:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired"
            )
        
        # Update password
        user.password = password_hash(reset_password_data.new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        self.db.commit()
        
        return success_response(
            message="Password has been reset successfully"
        )

    # Email Verification
    def verify_email(self, verification_data: EmailVerificationRequest):
        user = self.user_repo.get_by_field("email_verification_token", verification_data.token)
        
        if not user or not user.email_verification_token:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification token"
            )
        
        # Mark email as verified
        user.is_verified = True
        user.email_verification_token = None
        self.db.commit()
        
        return success_response(
            message="Email has been verified successfully"
        )

    # Change Password
    def change_password(self, user_id: int, change_password_data: ChangePasswordRequest):
        user = self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=ErrorMessages.USER_NOT_FOUND
            )
        
        # Verify current password
        if not verify_password(change_password_data.current_password, user.password):
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        # Update password
        user.password = password_hash(change_password_data.new_password)
        self.db.commit()
        
        return success_response(
            message="Password has been changed successfully"
        )
        