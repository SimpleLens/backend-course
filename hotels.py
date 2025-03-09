from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])
hotels_per_page = 2

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
def get_hotels(
        title: str | None = Query(default=None),
        name: str | None = Query(default=None),
        page: int = Query(default=0),
        per_page: int = Query(default=1)
):
    start_with = page*hotels_per_page-hotels_per_page if page != 0 else 0
    end_with = per_page*hotels_per_page
    
    return_hotels = []

    
    for i in range(start_with,end_with):
        try:
            return_hotels.append(hotels[i])
        except IndexError:
            break

    return return_hotels

    for hotel in hotels:
        if title and hotel['title'] != title:
            continue
        if name and hotel['name'] != name:
            continue
        return_hotels.append(hotel)
    
    return return_hotels


@router.post('')
def add_hotel(hotel: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value':{
        'title': 'Sochi', 'name': 'Сочи'
    }},
        '2': {'summary': 'Дубай', 'value':{
        'title': 'Dubai', 'name': 'Дубай'
    }}
})):
    global hotels

    hotels.append({'id': hotels[-1]['id']+1,
                   'title': hotel.title,
                   'name': hotel.name
    })

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


