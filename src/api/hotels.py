from fastapi import Query, Body, APIRouter

from src.api.dependencies import pagination_dep, DbDep
from src.schemas.hotels import HotelAddPut, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])

@router.get('', summary='получение отелей с фильтрацией и пагинацией')
async def get_hotels(
        Db: DbDep,
        pagination: pagination_dep,
        title: str | None = Query(default=None),
        location: str | None = Query(default=None)
):
    per_page = pagination.per_page or 5


    return await Db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=(pagination.page-1)*per_page)


@router.get('/{hotel_id}', summary='Получить конкретный отель по id')
async def get_hotel(
        Db: DbDep,
        hotel_id: int
    
):
    result = await Db.hotels.get_one(id = hotel_id)
    return result

@router.post('')
async def add_hotel(
        Db: DbDep, 
        hotel_data: HotelAddPut = Body(openapi_examples={
        '1': {'summary': 'Сочи', 'value':{
            'title': 'Sochi', 'location': 'Сочи'
        }},
            '2': {'summary': 'Дубай', 'value':{
            'title': 'Dubai', 'location': 'Дубай'
        }}
})):
 
    hotel = await Db.hotels.add(hotel_data)
    await Db.commit()
    
    return {'status':'OK', 'return': hotel}


@router.delete('/{hotel_id}')
async def delete_hotel(
        Db: DbDep,
        hotel_id: int   
):
    result = await Db.hotels.delete(id = hotel_id)
    await Db.commit()

    return result


@router.put("/{hotel_id}")
async def put_hotel(
        Db: DbDep,
        hotel_id: int,
        hotel: HotelAddPut
):
    result = await Db.hotels.edit(hotel,id = hotel_id)
    await Db.commit()

    return {"result":"OK", "hotel":result}


@router.patch("/{hotel_id}",
        summary='Частичное изменение отеля',
        description='Частичное изменение отеля, можно указать любой из параметров'
)
async def patch_hotel(
        Db: DbDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):

    await Db.hotels.edit(exclude_unset=True, data=hotel_data, id=hotel_id)
    await Db.commit() 

    return {'status':'OK'}


