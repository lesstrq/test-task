from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schemas import UserSchema, UserRegister, TokenInfo
from app.db.database import get_async_session
from app.db.models import User

import app.api.auth.utils as auth_utils
import app.db.utils as db_utils

from email_validator import validate_email, EmailNotValidError

auth_router = APIRouter(prefix="/auth")

async def validate_signup_data(
    username: str = Form(),
    email: str = Form(),
    password: str = Form(),
    password_repeat: str = Form()
):
    if password != password_repeat:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пароли не совпадают"
    )
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Указан некорректный адрес электронной почты"
    )
    return UserRegister(
        username=username,
        email=email,
        password=password
    )



@auth_router.post("/register", response_model=UserSchema)
async def register(
    fields: UserRegister = Depends(validate_signup_data), session: AsyncSession = Depends(get_async_session)
):
    new_user = User(
        email=fields.email,
        username=fields.username,
        password_hash=auth_utils.hash_password(fields.password),
    )

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    except Exception as e:
        print(str(e))
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Что-то пошло не так, попробуйте позже"
    )

    return UserSchema(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        signup_date=new_user.signup_date
    )


async def validate_auth_user(
    credential: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_async_session),
):
    unauhorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль"
    )
    if not (user := await db_utils.get_user(credential, session)):
        raise unauhorized_exception
    if auth_utils.validate_password(password, user.password_hash):
        return user
    raise unauhorized_exception


@auth_router.post("/login")
async def login(user: User = Depends(validate_auth_user), response_model=TokenInfo):
    jwt_payload = {"sub": str(user.id), "username": user.username, "email": user.email}
    access_token = auth_utils.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")

