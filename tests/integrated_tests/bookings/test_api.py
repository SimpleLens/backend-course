

async def test_add_booking(authenticated_ac, db):
    room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id": room_id,
            "date_from":"2024-10-11",
            "date_to":"2024-10-17"
        }
    )

    res_json = response.json()

    assert response.status_code == 200
    assert isinstance(res_json, dict)
    assert res_json["status"] == "OK"
