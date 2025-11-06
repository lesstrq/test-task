from fastapi import FastAPI
from app.api.auth.router import auth_router
from app.api.user.router import users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)