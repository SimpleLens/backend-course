


from src.api.dependencies import UserIdDep
from src.exceptions import AllRoomsAreBooked, DatesAreNotSuitableException, HotelNotFoundException, ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService


class BookingsService(BaseService):
    async def add_booking(
        self, 
        user_id: UserIdDep, 
        booking_data: BookingAddRequest
    ):
        if booking_data.date_to <= booking_data.date_from :
            raise DatesAreNotSuitableException
        
        try:
            room_data = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException

        try:
            hotel_id = (await self.db.hotels.get_one(id=room_data.hotel_id)).id
        except ObjectNotFoundException:
            raise HotelNotFoundException

        per_day_cost = room_data.price
        total_cost = per_day_cost * ((booking_data.date_to - booking_data.date_from).days)

        booking_data_to_add = BookingAdd(**booking_data.model_dump(), user_id=user_id, price=total_cost)

        try:
            added_booking = await self.db.bookings.add_booking(booking_data_to_add, hotel_id=hotel_id)
        except AllRoomsAreBooked as ex:
            raise ex
        
        await self.db.commit()
        
        return added_booking
    
    async def get_all_bookings(self):
        all_bookings = await self.db.bookings.get_all()

        return all_bookings

    async def get_my_bookings(self, user_id: UserIdDep):
        user_bookings = await self.db.bookings.get_filtered(user_id=user_id)

        return user_bookings
        