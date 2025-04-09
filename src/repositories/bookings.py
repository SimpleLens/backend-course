from datetime import date

from sqlalchemy import select
from pydantic import BaseModel
from fastapi import HTTPException

from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking
from src.models.bookings import BookingsModel
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_to_get
from src.schemas.bookings import BookingAdd

class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def get_bookings_with_todays_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )

        res = await self.session.execute(query)

        return [self.mapper.map_to_domen_entity(booking) for booking in res.scalars().all()]
    

    async def add_booking(
            self,
            booking: BookingAdd,
            hotel_id: int
        ):
        available_rooms_query = rooms_ids_to_get(date_to=booking.date_to, date_from=booking.date_from, hotel_id=hotel_id)
        
        result = await self.session.execute(available_rooms_query)

        rooms_ids = result.scalars().all()

        if booking.room_id in rooms_ids:
            result = await self.add(booking)
            return result
        
        raise HTTPException(500, detail="Все номера заняты")
        