from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking
from src.models.bookings import BookingsModel
from src.repositories.mappers.mappers import BookingDataMapper

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