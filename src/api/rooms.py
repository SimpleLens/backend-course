from datetime import date

from fastapi import APIRouter, Body, HTTPException

from services.rooms import RoomsService
from src.schemas.rooms import (
    Room,
    RoomAdd,
    RoomAddForRequest,
    RoomPut,
    RoomPatch,
    RoomPatchRequest,
    RoomPutRequest,
)
from src.api.dependencies import DbDep
from src.schemas.facilities import AddRoomFacility
from src.exceptions import DatesAreNotSuitableException, DatesAreNotSuitableHTTPException, HotelNotFoundException, HotelNotFoundHTTPException, ObjectNotFoundException, RoomNotFoundException, RoomNotFoundHTTPException

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
        added_room = await RoomsService(Db).add_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "room": added_room}


@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(Db: DbDep, hotel_id: int, date_from: date, date_to: date):
    try:
        rooms = await RoomsService(Db).get_rooms(hotel_id, date_from, date_to)
    except DatesAreNotSuitableException:
        raise DatesAreNotSuitableHTTPException

    return {"rooms": rooms}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный номер отеля")
async def get_one_room(Db: DbDep, hotel_id: int, room_id: int):
    try:
        rooms = await RoomsService(Db).get_one_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"rooms": rooms}


@router.put("/{hotel_id}/rooms/{room_id}")
async def full_edit_rooms(Db: DbDep, hotel_id: int, room_id: int, room_data: RoomPutRequest):
    try:
        await RoomsService(Db).full_edit_rooms(hotel_id=hotel_id,room_data=room_data, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def particially_edit_rooms(
    Db: DbDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    try:
        await RoomsService(Db).particially_edit_rooms(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(Db: DbDep, hotel_id: int, room_id: int):
    try:
        await RoomsService(Db).delete_room(hotel_id=hotel_id,room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK"}
