import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import Session
from sqlalchemy import delete
from collections.abc import AsyncGenerator

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.schemas import UserCreate
from app.db.models import User

from tests.utils.utils import (
    get_superuser_token_headers,
    create_random_user,
    user_authentication_headers,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[Session, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[
    AsyncClient,
    None,
]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test" + settings.API_V1_STR
    ) as c:
        yield c


@pytest_asyncio.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture(scope="module")
async def normal_user(db: Session) -> UserCreate:
    user: UserCreate = create_random_user(db)
    return user


@pytest_asyncio.fixture(scope="module")
async def normal_user_token_headers(
    client: AsyncClient, normal_user: UserCreate
) -> dict[str, str]:
    return await user_authentication_headers(
        client=client, email=normal_user.email, password=normal_user.password
    )
