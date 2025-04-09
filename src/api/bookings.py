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
    room_data = await Db.rooms.get_one_or_none(room_id = booking_data.room_id)

    if not room_data:
        raise HTTPException(404, "Комната не найдена")
    
    hotel_id = (await Db.hotels.get_one_or_none(id=room_data.hotel_id)).id

    if not room_data:
        raise HTTPException(404, "Отель с такой комнатой не найден")

    per_day_cost = room_data.price
    total_cost = per_day_cost * ((booking_data.date_to - booking_data.date_from).days)

    booking_data_to_add = BookingAdd(**booking_data.model_dump(), user_id=user_id,price=total_cost)

    added_booking = await Db.bookings.add_booking(booking_data_to_add, hotel_id = hotel_id)
    await Db.commit()

    return {"status":"OK", "booking": added_booking}


@router.get("", summary="Получить все бронирования")
async def get_all_bookings(
        Db: DbDep
):
    all_bookings = await Db.bookings.get_all()

    return all_bookings

@router.get("/me", summary="Получить бронирования аутентифицированного пользователя")
async def get_my_bookings(
    Db: DbDep,
    user_id: UserIdDep
):
    user_bookings = await Db.bookings.get_filtered(user_id = user_id)

    return user_bookings
    

