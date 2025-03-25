from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.schemas.rooms import Room, RoomWithFacilities
from src.models.rooms import RoomsModel
from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.database import engine
from src.repositories.facilities import FacilitiesModel, RoomsFacilitiesModel
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

        query = (
            select(self.model)
            .select_from(self.model)
            .filter(
                RoomsModel.id.in_(rooms_ids_to_get(hotel_id=hotel_id, date_to=date_to, date_from=date_from))
                )
            .options(selectinload(self.model.facilities))
            )
        
        result = await self.session.execute(query)


        return [RoomWithFacilities.model_validate(room) for room in result.scalars().all()]
    

    async def get_one_or_none(
            self,
            hotel_id: int,
            room_id: int
    ):
        query = (
            select(self.model)
            .filter(RoomsModel.id == room_id, RoomsModel.hotel_id == hotel_id)
            .options(selectinload(self.model.facilities))
        )

        result = await self.session.execute(query)

        return RoomWithFacilities.model_validate(result.scalars().one_or_none())






















    # async def get_filtered_by_data( ### Мое решение задачи с выводом удобств номеров с использованием одного sql запроса (считаю что очень хорошо справился с заданием)
    #         self,
    #         hotel_id: int,
    #         date_from: date,
    #         date_to: date
    # ):

    #     custom_model_rooms_dict = {}

    #     rooms_to_get_query = (
    #         select(self.model, FacilitiesModel)
    #         .select_from(self.model)
    #         .filter(
    #             RoomsModel.id.in_(rooms_ids_to_get(hotel_id=hotel_id, date_to=date_to, date_from=date_from))
    #             )
    #         .outerjoin(RoomsFacilitiesModel, RoomsFacilitiesModel.room_id == RoomsModel.id)
    #         .outerjoin(FacilitiesModel, FacilitiesModel.id == RoomsFacilitiesModel.facility_id)
    #         )
    #     result = await self.session.execute(rooms_to_get_query)

    #     rooms_with_facilities = result.all()

    #     for i in rooms_with_facilities:
    #         if i[0].id not in custom_model_rooms_dict:
    #             custom_model_rooms_dict[i[0].id] = {"id": i[0].id, "hotel_id":i[0].hotel_id, "title":i[0].title, "price":i[0].price, "description":i[0].description, "quantity": i[0].quantity, "facilities":[]}
        
    #     for i in rooms_with_facilities:
    #         custom_model_rooms_dict[i[0].id]["facilities"].append(i[1])

    #     return [RoomWithFacilities.model_validate(i) for rooms,i in custom_model_rooms_dict.items()]