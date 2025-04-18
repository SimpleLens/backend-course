from datetime import date

from fastapi import APIRouter, Body, HTTPException

from src.schemas.rooms import (
    RoomAdd,
    RoomAddForRequest,
    RoomPut,
    RoomPatch,
    RoomPatchRequest,
    RoomPutRequest,
)
from src.api.dependencies import DbDep
from src.schemas.facilities import AddRoomFacility
from src.exceptions import ObjectNotFoundException

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.post("/{hotel_id}/rooms")
async def add_room(
    Db: DbDep,
    hotel_id: int,
    room_data: RoomAddForRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Крутой номер",
                "value": {
                    "title": "Очень крутой номер",
                    "price": 1000,
                    "description": ".",
                    "quantity": 10,
                    "facilities_ids": [2, 3],
                },
            }
        }
    ),
):
    try:
        await Db.hotels.get_one(id = hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Отель не найден")

    data_to_add = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude="facilities_ids"))

    added_room = await Db.rooms.add(data_to_add)

    facilities_to_add = [
        AddRoomFacility(room_id=added_room.id, facility_id=i) for i in room_data.facilities_ids
    ]
    await Db.rooms_facilities.add_bulk(facilities_to_add)

    await Db.commit()

    return {"status": "OK", "room": added_room}


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(Db: DbDep, hotel_id: int, date_from: date, date_to: date):
    if date_to < date_from:
        raise HTTPException(400, detail="Дата выезда не может быть раньше даты заезда")
    
    rooms = await Db.rooms.get_filtered_by_data(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )

    return {"rooms": rooms}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный номер отеля")
async def get_rooms(Db: DbDep, hotel_id: int, room_id: int):
    try:
        rooms = await Db.rooms.get_one(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Номер не найден")

    return {"rooms": rooms}


@router.put("/{hotel_id}/rooms/{room_id}")
async def full_edit_rooms(Db: DbDep, hotel_id: int, room_id: int, room_data: RoomPutRequest):
    data_to_update = RoomPut(**room_data.model_dump(exclude="facilities_ids"))
    try:
        await Db.rooms.get_one(id = room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Комната не найдена")
    
    await Db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await Db.rooms.edit(data_to_update, exclude_unset=True, hotel_id=hotel_id, id=room_id)

    await Db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def particially_edit_rooms(
    Db: DbDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    try:
        await Db.rooms.get_one(id = room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Комната не найдена")
    
    room_data_dict_for_facilities = room_data.model_dump(exclude_unset=True)

    room_data_to_update = RoomPatch(room_data.model_dump(exclude="facilities_ids"))

    if "facilities_ids" in room_data_dict_for_facilities:
        await Db.rooms_facilities.set_facilities(
            room_id=room_id,
            facilities_ids=room_data_dict_for_facilities["facilities_ids"],
        )

    await Db.rooms.edit(room_data_to_update, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await Db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(Db: DbDep, hotel_id: int, room_id: int):
    try:
        await Db.rooms.delete(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Комната не найдена")
    
    await Db.commit()

    return {"status": "OK"}
