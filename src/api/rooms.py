from datetime import date

from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomAddForRequest, RoomPut, RoomPatch, RoomPatchRequest
from src.api.dependencies import DbDep
from src.schemas.facilities import AddRoomFacility

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.post("/{hotel_id}/rooms")
async def add_room(
        Db: DbDep,
        hotel_id: int,
        room_data: RoomAddForRequest = Body(openapi_examples={
            "1": {"summary":"Крутой номер","value":{
                "title": "Очень крутой номер",
                "price": 1000,
                "description": ".",
                "quantity": 10,
                "facilities_ids": [2,3]
            }}
        })
):
    data_to_add = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude="facilities_ids"))
    added_room = await Db.rooms.add(data_to_add)

    facilities_to_add = [AddRoomFacility(room_id=added_room.id, facility_id=i) for i in room_data.facilities_ids]
    await Db.rooms_facilities.add_bulk(facilities_to_add)

    await Db.commit()

    return {"status": "OK", "room": added_room}


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(
        Db: DbDep,
        hotel_id: int,
        date_from: date,
        date_to: date
):
    rooms = await Db.rooms.get_filtered_by_data(hotel_id = hotel_id, date_from=date_from, date_to=date_to)

    return {"rooms": rooms}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный номер отеля")
async def get_rooms(
        Db: DbDep,
        hotel_id: int,
        room_id: int
):
    rooms = await Db.rooms.get_one_or_none(hotel_id = hotel_id, id=room_id)

    return {"rooms": rooms}


@router.put("/{hotel_id}/rooms/{room_id}")
async def full_edit_rooms(
        Db: DbDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPut
):
    await Db.rooms.edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await Db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def particially_edit_rooms(
        Db: DbDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    facilities = await Db.rooms_facilities.get_filtered(room_id = room_id)
    existing_facilities = [i.facility_id for i in facilities]
    ids_of_facil = [i.id for i in facilities]
    facilities_from_request = room_data.facilities_ids
    facilities_to_delete = []
    #1234
    #235
    for i in existing_facilities:
        if i in facilities_from_request:
            facilities_from_request.remove(i)
            continue

        facilities_to_delete.append(ids_of_facil[existing_facilities.index(i)])

    facilities_to_add = [AddRoomFacility(facility_id=i, room_id=room_id) for i in facilities_from_request]
    
    if facilities_to_add:
        await Db.rooms_facilities.add_bulk(facilities_to_add)
    
    if facilities_to_delete:
        await Db.rooms_facilities.delete_bulk(facilities_to_delete)

    room_data_to_update = RoomPatch(**room_data.model_dump(exclude="facilities_ids"))

    await Db.rooms.edit(room_data_to_update, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await Db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        Db: DbDep,
        hotel_id: int,
        room_id: int
):
    await Db.rooms.delete(hotel_id = hotel_id, id = room_id)
    await Db.commit()   

    return {"status": "OK"}
