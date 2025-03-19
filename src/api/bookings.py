from fastapi import APIRouter, HTTPException

from src.api.dependencies import UserIdDep, DbDep
from src.schemas.bookings import Booking, BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(
        Db: DbDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest
): 
    room_data = await Db.rooms.get_one_or_none(id = booking_data.room_id)

    if not room_data:
        raise HTTPException(404, "Комната не найдена")
    
    per_day_cost = room_data.price
    total_cost = per_day_cost * (booking_data.date_to - booking_data.date_from).days

    booking_data_to_add = BookingAdd(**booking_data.model_dump(), user_id=user_id,price=total_cost)

    added_booking = await Db.bookings.add(booking_data_to_add)
    await Db.commit()

    return {"status":"OK", "booking": added_booking}
    

