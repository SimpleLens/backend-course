from fastapi import APIRouter, HTTPException

from src.models.bookings import BookingsModel
from src.services.bookings import BookingsService
from src.api.dependencies import UserIdDep, DbDep
from src.schemas.bookings import Booking, BookingAddRequest, BookingAdd
from src.exceptions import AllRoomsAreBookedHTTPException, DatesAreNotSuitableException, DatesAreNotSuitableHTTPException, HotelNotFoundException, HotelNotFoundHTTPException, ObjectNotFoundException, AllRoomsAreBooked, RoomNotFoundException, RoomNotFoundHTTPException

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(
    Db: DbDep, 
    user_id: UserIdDep, 
    booking_data: BookingAddRequest
):
    try:
        added_booking = await BookingsService(Db).add_booking(user_id=user_id,booking_data=booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except DatesAreNotSuitableException:
        raise DatesAreNotSuitableHTTPException
    except AllRoomsAreBooked:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "booking": added_booking}


@router.get("", summary="Получить все бронирования")
async def get_all_bookings(Db: DbDep):
    all_bookings = await BookingsService(Db).get_all_bookings()

    return all_bookings


@router.get("/me", summary="Получить бронирования аутентифицированного пользователя")
async def get_my_bookings(Db: DbDep, user_id: UserIdDep):
    user_bookings = await BookingsService(Db).get_my_bookings(user_id=user_id)

    return user_bookings
