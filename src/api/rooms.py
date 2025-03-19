from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomAddForRequest, RoomPut, RoomPatch
from src.api.dependencies import DbDep

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.post("/{hotel_id}/rooms")
async def add_room(
        Db: DbDep,
        hotel_id: int,
        room_data: RoomAddForRequest = Body(openapi_examples={
            "1": {"summary":"Крутой номер","value":{
                "hotel_id": 5,
                "title": "Очень крутой номер",
                "price": 1000,
                "description": ".",
                "quantity": 10
            }}
        })
):
    data_to_add = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    added_room = await Db.rooms.add(data_to_add)
    await Db.commit()

    return {"status": "OK", "room": added_room}


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(
        Db: DbDep,
        hotel_id: int
):
    rooms = await Db.rooms.get_all(hotel_id = hotel_id)

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
        room_data: RoomPatch
):
    await Db.rooms.edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
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
