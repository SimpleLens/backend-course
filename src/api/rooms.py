from fastapi import APIRouter, Body

from src.schemas.rooms import RoomAdd, RoomAddForRequest, RoomPut, RoomPatch
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.post("/{hotel_id}/rooms")
async def add_room(
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
    async with async_session_maker() as session:
        added_room = await RoomsRepository(session).add(data_to_add)
        await session.commit()

    return {"status": "OK", "room": added_room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int
):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(hotel_id = hotel_id)

    return {"rooms": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_rooms(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(hotel_id = hotel_id, id=room_id)

    return {"rooms": rooms}


@router.put("/{hotel_id}/rooms/{room_id}")
async def full_edit_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomPut
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def particially_edit_rooms(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatch
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id = hotel_id, id = room_id)
        await session.commit()   

    return {"status": "OK"}
