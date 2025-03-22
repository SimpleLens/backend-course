from datetime import date

from sqlalchemy import func, select

from src.schemas.rooms import Room
from src.models.rooms import RoomsModel
from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.database import engine
from src.repositories.utils import rooms_ids_to_get

class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_filtered_by_data(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        rooms = await self.get_filtered(RoomsModel.id.in_(rooms_ids_to_get(hotel_id, date_to, date_from)))

        return rooms