from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from app.config.settings import Setting
from typing import Optional
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status as http_status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.messages import ErrorMessages, SuccessMessages

# Security scheme for Bearer tokens
security = HTTPBearer()

# Generate Token 
def generate_token(data: dict, expiry_time_in_min: Optional[int] = 60):

    # Calculate expiry time based on expiry_time_in_min
    expiry_time = int((datetime.now(timezone.utc) + timedelta(minutes=expiry_time_in_min)).timestamp())

    # Check JWT payload is available
    if not data:
        raise HTTPException(
            status_code = http_status.HTTP_406_NOT_ACCEPTABLE,
            detail=ErrorMessages.PAYLOAD_REQUIRED
        )

    # Add expiry time to data
    data['exp'] = expiry_time

    # Generate JWT token
    token = jwt.encode(data, key=Setting.JWT_SECRET, algorithm=Setting.JWT_ALGORITHM )

    return token

# Validate token 
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Extract token from Bearer credentials
        token = credentials.credentials
        
        # Decode token using Secret key
        payload = jwt.decode(token=token,key=Setting.JWT_SECRET, algorithms=Setting.JWT_ALGORITHM)
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.JWT_EXPIRY
        )

    except JWTError:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.JWT_ERROR
        )

    except Exception as e:
        raise HTTPException(
            status_code= http_status.HTTP_401_UNAUTHORIZED,
            detail=f"Error : {str(e)}"
        )