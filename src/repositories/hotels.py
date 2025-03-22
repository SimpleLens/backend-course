from datetime import date

from sqlalchemy import select, insert
from sqlalchemy import func

from src.models.hotels import HotelsOrm 
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel 
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_ids_to_get

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(
            self,
            date_to: date,
            date_from: date,
            offset: int,
            limit: int,
            location: str | None = None,
            title: str | None = None
    ):
        available_rooms = rooms_ids_to_get(date_to=date_to, date_from=date_from)

        hotels_to_get = (
            select(RoomsModel.hotel_id)
            .filter(RoomsModel.id.in_(available_rooms))
        )
        query_to_get_hotels = (
            select(HotelsOrm)
            .select_from(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_to_get))
            .limit(limit)
            .offset(offset)
        )

        if title:
            query_to_get_hotels = query_to_get_hotels.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query_to_get_hotels = query_to_get_hotels.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        result = await self.session.execute(query_to_get_hotels)

        if result:
            return [Hotel.model_validate(hotel) for hotel in result.scalars().all()]
        return None