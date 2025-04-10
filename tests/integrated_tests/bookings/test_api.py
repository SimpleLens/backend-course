import pytest
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async with DBManager(async_session_maker_null_pool) as db_:
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    "date_from, date_to, room_id, status_code",
    [
        ("2024-10-11", "2024-10-20", 1, 200),
        ("2024-10-13", "2024-10-21", 1, 200),
        ("2024-10-15", "2024-10-19", 1, 200),
        ("2024-10-15", "2024-10-20", 1, 200),
        ("2024-10-18", "2024-10-26", 1, 200),
        ("2024-10-11", "2024-10-20", 1, 500),
        ("2024-11-14", "2024-11-17", 1, 200),
    ],
)
async def test_add_booking(date_from, date_to, room_id, status_code, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    res_json = response.json()

    assert response.status_code == status_code

    if status_code == 200:
        assert isinstance(res_json, dict)
        assert res_json["status"] == "OK"


@pytest.mark.parametrize(
    "date_from, date_to, room_id, count_of_bookings",
    [
        ("2024-10-11", "2024-10-20", 1, 1),
        ("2024-10-13", "2024-10-21", 1, 2),
        ("2024-10-15", "2024-10-19", 1, 3),
    ],
)
async def test_get_after_adding_bookings(
    room_id,
    date_from,
    date_to,
    count_of_bookings,
    authenticated_ac,
    delete_all_bookings,
):
    response_add = await authenticated_ac.post(
        "/bookings",
        json={"date_to": date_to, "date_from": date_from, "room_id": room_id},
    )

    assert response_add.status_code == 200

    response_get_all = await authenticated_ac.get("/bookings/me")

    assert response_get_all.status_code == 200
    assert len(response_get_all.json()) == count_of_bookings
