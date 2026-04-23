from app.routes.user_routes import router as UserRouter
from app.routes.auth_routes import router as AuthRouter
from app.routes.essay_routes import router as EssayRouter
from fastapi import APIRouter

router = APIRouter(
    prefix= "/api/v1"
)

router.include_router(UserRouter, prefix="/users", tags=["users"])
router.include_router(AuthRouter, prefix="/auth", tags=["authentication"])
router.include_router(EssayRouter, prefix="/essays", tags=["essays"])
