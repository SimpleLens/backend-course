

from datetime import date
from src.schemas.hotels import HotelAddPut, HotelPATCH
from src.api.dependencies import Pagination
from src.services.base import BaseService


class HotelService(BaseService):

    async def get_hotels_by_data(
        self,
        pagination: Pagination,
        date_from: date,
        date_to: date,
        title: str | None,
        location: str | None,
    ):
        
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtered_by_time(
            date_to=date_to,
            date_from=date_from,
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )
    

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)
    

    async def create_hotel(self, hotel_data: HotelAddPut):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()

        return hotel
    

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    
    async def full_hotel_edit(
        self,
        hotel_id: int,          
        hotel: HotelAddPut
    ):
        result = await self.db.hotels.edit(hotel, id=hotel_id)
        await self.db.commit()

        return result
    

    async def partitially_hotel_edit(
        self,
        hotel_id: int,          
        hotel_data: HotelPATCH
    ):
        await self.db.hotels.edit(exclude_unset=True, data=hotel_data, id=hotel_id)
        await self.db.commit()   

