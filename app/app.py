from fastapi import FastAPI
from .api.user import router as user_router
from .api.auth import router as auth_router

app = FastAPI(title="School Diary API")

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
