from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session
from app.schema.user_schema import UserRegistration
from app.services.user_service import UserService
from app.db.session import get_db
from app.utils.response import error_response
from app.utils.messages import ErrorMessages

router = APIRouter()

@router.post("/")
def register_user(data: UserRegistration, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        return user_service.user_registration(user_data=data.model_dump())
    except HTTPException as e:
        return error_response(
            status_code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return error_response(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=ErrorMessages.INTERNAL_SERVER_ERROR.format(
                e = e
            )
        )