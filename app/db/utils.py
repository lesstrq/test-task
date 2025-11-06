from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User

async def get_user(credential: str | int, session: AsyncSession) -> User | None:
    if isinstance(credential, int):
        return await get_user_by_id(id=credential, session=session)
    if isinstance(credential, str):
        if "@" in credential:
            get_by_email = await get_user_by_email(email=credential, session=session)
            if get_by_email:
                return get_by_email
        get_by_username = await get_user_by_username(
            username=credential, session=session
        )
        return get_by_username

async def get_user_by_id(id: int, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.id == id))
    user = result.first()
    return user[0] if user else None

async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    user = result.first()
    return user[0] if user else None


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.first()
    return user[0] if user else None
