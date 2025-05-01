import json

import pytest
from unittest import mock
from httpx import ASGITransport, AsyncClient

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda a: a).start()

from src.main import app
from src.database import engine_null_pool, Base
from src.models import *
from src.config import settings
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.models.rooms import RoomsModel
from src.models.hotels import HotelsModel
from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAddPut
from src.api.dependencies import getDB


async def db_overrides():
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[getDB] = db_overrides


@pytest.fixture(scope="session")
async def check_for_test():
    assert settings.MODE == "TEST"


@pytest.fixture()
async def db():
    async with DBManager(async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_for_test):
    async with engine_null_pool.begin() as sesison:
        await sesison.run_sync(Base.metadata.drop_all)
        await sesison.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", "r", encoding="utf-8") as file:
        hotels = [HotelAddPut.model_validate(hotel) for hotel in json.load(file)]

    with open("tests/mock_rooms.json", "r", encoding="utf-8") as file:
        rooms = [RoomAdd.model_validate(room) for room in json.load(file)]

    async with DBManager(async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)

        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def registrate_user(ac, setup_database):
    response = await ac.post(
        "auth/register", json={"email": "penisnostb@gmail.ru", "password": "12345"}
    )

    assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, registrate_user):
    response = await ac.post("/auth/login", json={"email": "penisnostb@gmail.ru", "password": "12345"})

    assert ac.cookies.get("access_token")
    assert response.status_code == 200

    yield ac
