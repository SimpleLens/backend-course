from datetime import datetime

from src.schemas.bookings import BookingAdd


async def test_bookings_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    date_from = datetime(year=2024, month=12, day=12)
    date_to = datetime(year=2024, month=12, day=15)

    booking = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=10000,
    )

    booking_update = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=500,
    )

    await db.bookings.add(booking)

    added_booking = await db.bookings.get_one_or_none(date_from=date_from, date_to=date_to)

    assert added_booking

    await db.bookings.edit(booking_update, date_from=date_from, date_to=date_to)

    await db.bookings.delete(price=500, date_from=date_from, date_to=date_to)

    deleted_booking = await db.bookings.get_one_or_none(
        price=500, date_from=date_from, date_to=date_to
    )

    assert not deleted_booking
