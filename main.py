from fastapi import FastAPI, Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import get_db
from app.db import models
from app.utils.jwt import generate_token, validate_token
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

# Middleware
class AuthMidd(BaseHTTPMiddleware):
    def dispatch(self, request: Request, call_next):
        response = call_next(request)
        return response


app = FastAPI(
    title="LLM API Server",
    summary="This Server contains LLM Integration",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 👈 allow all origins
    allow_credentials=True,
    allow_methods=["*"],   # allow all HTTP methods
    allow_headers=["*"],   # allow all headers
)

app.add_middleware(AuthMidd)
app.include_router(router, prefix="/backend")

@app.get("/hello")
def hello(db = Depends(get_db)):

    data = {
        "name" : "vraj",
        "std" : 12, 
        "auth": "hello"
    }

    # token =  generate_token(data)
    token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidnJhaiIsInN0ZCI6MTIsImF1dGgiOiJoZWxsbyIsImV4cCI6MTc3NjY3OTA0NH0.aeaRIkQ6IfTNq1oFPjBL0ZL4XCccWOVuJhE4FC2YC-s"

    payload = validate_token(token)

    return {
        "msg": token,
        "payload" : payload
    }

