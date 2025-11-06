from fastapi import APIRouter, Depends
from app.api.user.schemas import UserSchema
from app.api.auth.utils import get_current_auth_user


users_router = APIRouter(prefix="/users")


@users_router.post("/profile", response_model=UserSchema)
async def profile(user: UserSchema = Depends(get_current_auth_user)):
    return user