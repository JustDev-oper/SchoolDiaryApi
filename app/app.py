from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.user import router as user_router
from .api.auth import router as auth_router

app = FastAPI(title="School Diary API")

# список доменов, с которых можно слать запросы
origins = [
    "http://localhost:3000",   # Vite dev-сервер
    "http://127.0.0.1:3000",   # иногда используется этот
]

# 👇 Важно — используем именно класс CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,   # нужно для работы HttpOnly cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

# роутеры
app.include_router(user_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
