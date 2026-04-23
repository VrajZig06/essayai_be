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

@app.get("/health")
def hello():

    return {
        "msg": "Yeah, I am Helthy!"
    }

