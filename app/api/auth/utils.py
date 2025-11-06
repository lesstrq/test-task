from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.api.auth.schemas import UserSchema
import jwt
import bcrypt
from app.core.config import settings
from datetime import timedelta, datetime, UTC
from app.db.utils import get_user_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session

http_bearer = HTTPBearer()


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
    token_type: str = "access"
):
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now, type=token_type)
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> UserSchema:
    id = payload.get("sub")
    if id.isdigit():
        id = int(id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
        )
    user = await get_user_by_id(id, session)
    if user:
        return UserSchema(
            id=user.id,
            email=user.email,
            username=user.username,
            signup_date=user.signup_date,
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
    )
