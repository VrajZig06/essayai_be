import email
from pydantic import BaseModel, model_validator, EmailStr
from typing import Literal, Optional
from app.utils.messages import ErrorMessages, SuccessMessages

class UserRegistration(BaseModel):
    first_name: str
    last_name: str

    type: Literal['p','e']

    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_verified: Optional[bool] = False

    password: str


    @model_validator(mode="after")
    def check_type_based_input(self):
        if self.type == "p" and self.phone is None:
            raise ValueError(ErrorMessages.PHONE_NUMBER_REQUIRED)
        elif self.type == "e" and self.email is None:
            raise ValueError(ErrorMessages.EMAIL_REQUIRED)
        
        return self
    
class UserRegistartionResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    type: str

    model_config = {
        "from_attributes" : True
    }

# Authentication Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRegistartionResponse

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class EmailVerificationRequest(BaseModel):
    token: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str 

