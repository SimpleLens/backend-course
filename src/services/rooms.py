

from datetime import date
from src.exceptions import DatesAreNotSuitableHTTPException, DatesAreNotSuitableException, HotelNotFoundException, ObjectNotFoundException, RoomNotFoundException
from src.schemas.facilities import AddRoomFacility
from src.schemas.rooms import RoomAdd, RoomAddForRequest, RoomPatch, RoomPatchRequest, RoomPut, RoomPutRequest
from src.services.base import BaseService


class RoomsService(BaseService):
    async def add_room(
    self,
    hotel_id: int,
    room_data: RoomAddForRequest
):
        try:
            await self.db.hotels.get_one(id = hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

        data_to_add = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude="facilities_ids"))

        added_room = await self.db.rooms.add(data_to_add)

        facilities_to_add = [
            AddRoomFacility(room_id=added_room.id, facility_id=i) for i in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(facilities_to_add)

        await self.db.commit()

        return added_room

    async def get_rooms(self, hotel_id: int, date_from: date, date_to: date):
        if date_to < date_from:
            raise DatesAreNotSuitableException
        
        
        rooms = await self.db.rooms.get_filtered_by_data(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        return rooms

    async def get_one_room(self, hotel_id: int, room_id: int):
        try:
            rooms = await self.db.rooms.get_one(hotel_id=hotel_id, id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        
        return rooms

    async def full_edit_rooms(self, hotel_id: int, room_id: int, room_data: RoomPutRequest):
        data_to_update = RoomPut(**room_data.model_dump(exclude="facilities_ids"))
        try:
            await self.db.rooms.get_one(id = room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        
        await self.db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
        await self.db.rooms.edit(data_to_update, exclude_unset=True, hotel_id=hotel_id, id=room_id)

        await self.db.commit()

    async def particially_edit_rooms(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ):
        try:
            await self.db.rooms.get_one(id = room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        
        room_data_dict_for_facilities = room_data.model_dump(exclude_unset=True)

        room_data_to_update = RoomPatch(room_data.model_dump(exclude="facilities_ids"))

        if "facilities_ids" in room_data_dict_for_facilities:
            await self.db.rooms_facilities.set_facilities(
                room_id=room_id,
                facilities_ids=room_data_dict_for_facilities["facilities_ids"],
            )

        await self.db.rooms.edit(room_data_to_update, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await self.db.commit()
    
    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        
        await self.db.commit()