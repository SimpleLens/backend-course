from fastapi import Query, Body, APIRouter, Depends
from schemas.hotels import Hotel, HotelPATCH
from typing import Annotated

from src.api.dependencies import pagination_dep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelAdd
from src.repositories.hotels import HotelsRepository


router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('', summary='получение отелей с фильтрацией и пагинацией')
async def get_hotels(
        pagination: pagination_dep,
        title: str | None = Query(default=None),
        location: str | None = Query(default=None)
):
    per_page = pagination.per_page or 5

    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page-1)*per_page)

@router.get('/{hotel_id}', summary='Получить конкретный отель по id')
async def get_hotel(
    hotel_id: int
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_one(id = hotel_id)
    return result

@router.post('')
async def add_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value':{
        'title': 'Sochi', 'location': 'Сочи'
    }},
        '2': {'summary': 'Дубай', 'value':{
        'title': 'Dubai', 'location': 'Дубай'
    }}
})):
 
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {'status':'OK', 'return': hotel}


@router.delete('/{hotel_id}')
async def delete_hotel(
        hotel_id: int   
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete(id = hotel_id)
        await session.commit()

    return result


@router.put("/{hotel_id}")
async def put_hotel(
        hotel_id: int,
        hotel: HotelAdd
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).edit(hotel,id = hotel_id)
        await session.commit()

    return result


@router.patch("/{hotel_id}",
        summary='Частичное изменение отеля',
        description='Частичное изменение отеля, можно указать любой из параметров'
)
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(exclude_unset=True, data=hotel_data, id=hotel_id)
        await session.commit() 

    return {'status':'OK'}


