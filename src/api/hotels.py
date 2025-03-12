from fastapi import Query, Body, APIRouter, Depends
from schemas.hotels import Hotel, HotelPATCH
from typing import Annotated
from sqlalchemy import insert, select

from src.api.dependencies import pagination_dep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1,'title':'dubai','name':'дубай'},
    {'id': 2,'title':'sochi','name':'сочи'},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"}
    ]


@router.get('')
async def get_hotels(
        pagination: pagination_dep,
        title: str | None = Query(default=None),
        name: str | None = Query(default=None)
):

    return_hotels = []  

    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        return result.scalars().all()

    if pagination.page and pagination.per_page:
        pagination_hotels = []
        for i in range((pagination.page-1)*pagination.per_page, pagination.per_page*pagination.page):
            pagination_hotels.append(return_hotels[i])
        return pagination_hotels

    return return_hotels


@router.post('')
async def add_hotel(hotel: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value':{
        'title': 'Sochi', 'location': 'Сочи'
    }},
        '2': {'summary': 'Дубай', 'value':{
        'title': 'Dubai', 'location': 'Дубай'
    }}
})):
 
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status':'OK'}


@router.delete('/{hotel_id}')
def delete_hotel(
        hotel_id: int
):
    global hotels
    
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]

    return {'status':'OK'}


@router.put("/{hotel_id}")
def put_hotel(
    hotel_id: int,
    hotel: Hotel
):
    global hotels

    hotels[hotel_id-1] = {'id': hotel_id, 'title': hotel.title, 'name': hotel.name}

    return {'status':'OK'}


@router.patch("/{hotel_id}",
    summary='Частичное изменение отеля',
    description='Частичное изменение отеля, можно указать любой из параметров'
)
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels

    hotels[hotel_id-1] = {'id': hotel_id, 'title': hotel_data.title if hotel_data.title else hotels[hotel_id-1]['title'], 'name': hotel_data.name if hotel_data.name else hotels[hotel_id-1]['name']}

    return {'status':'OK'}


