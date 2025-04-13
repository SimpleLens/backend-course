from datetime import date

from sqlalchemy import select, insert
from sqlalchemy import func

from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_ids_to_get
from src.repositories.mappers.mappers import HotelDataMapper


class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_to: date,
        date_from: date,
        offset: int,
        limit: int,
        location: str | None = None,
        title: str | None = None,
    ):
        available_rooms = rooms_ids_to_get(date_to=date_to, date_from=date_from)

        hotels_to_get = select(RoomsModel.hotel_id).filter(RoomsModel.id.in_(available_rooms))
        query_to_get_hotels = (
            select(HotelsModel)
            .select_from(HotelsModel)
            .filter(HotelsModel.id.in_(hotels_to_get))
            .limit(limit)
            .offset(offset)
        )

        if title:
            query_to_get_hotels = query_to_get_hotels.filter(
                func.lower(HotelsModel.title).contains(title.strip().lower())
            )
        if location:
            query_to_get_hotels = query_to_get_hotels.filter(
                func.lower(HotelsModel.location).contains(location.strip().lower())
            )

        result = await self.session.execute(query_to_get_hotels)

        if result:
            return [self.mapper.map_to_domen_entity(hotel) for hotel in result.scalars().all()]
        return None
