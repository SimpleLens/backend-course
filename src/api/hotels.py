from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException

from services.hotels import HotelService
from src.api.dependencies import pagination_dep, DbDep
from src.schemas.hotels import HotelAddPut, HotelPATCH
from src.exceptions import ObjectNotFoundException

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="получение отелей с фильтрацией и пагинацией")
async def get_hotels(
    Db: DbDep,
    pagination: pagination_dep,
    date_from: date,
    date_to: date,
    title: str | None = Query(default=None),
    location: str | None = Query(default=None),
):
    if date_to <= date_from:
        raise HTTPException(400, detail="Дата выезда не может быть раньше даты заезда")

    return await HotelService(Db).get_hotels_by_data(
        pagination, 
        date_from, 
        date_to,
        title,
        location)


@router.get("/{hotel_id}", summary="Получить конкретный отель по id")
async def get_hotel(Db: DbDep, hotel_id: int):
    try:
        result = await HotelService(Db).get_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Отеля не существует")
    
    return result


@router.post("")
async def add_hotel(
    Db: DbDep,
    hotel_data: HotelAddPut = Body(
        openapi_examples={
            "1": {"summary": "Сочи", "value": {"title": "Sochi", "location": "Сочи"}},
            "2": {"summary": "Дубай", "value": {"title": "Dubai", "location": "Дубай"}},
        }
    ),
):

    return {"status": "OK", "return": await HotelService(Db).create_hotel(hotel_data)}


@router.delete("/{hotel_id}")
async def delete_hotel(Db: DbDep, hotel_id: int):
    await HotelService(Db).delete_hotel(hotel_id)

    return {"result": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(Db: DbDep, hotel_id: int, hotel_data: HotelAddPut):
    result = await HotelService(Db).full_hotel_edit(hotel_id, hotel_data)

    return {"result": "OK", "hotel": result}


@router.patch(
    "/{hotel_id}",
    summary="Частичное изменение отеля",
    description="Частичное изменение отеля, можно указать любой из параметров",
)
async def patch_hotel(Db: DbDep, hotel_id: int, hotel_data: HotelPATCH):
    await HotelService(Db).partitially_hotel_edit(hotel_id, hotel_data)

    return {"status": "OK"}
