from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {'id': 1,'title':'dubai','name':'дубай'},
    {'id': 2,'title':'sochi','name':'сочи'}
    ]


@app.get('/hotels')
def get_hotels(
        title: str | None = Query(default=None),
        name: str | None = Query(default=None)
):
    return_hotels = []
    for hotel in hotels:
        if title and hotel['title'] != title:
            continue
        if name and hotel['name'] != name:
            continue
        return_hotels.append(hotel)
    
    return return_hotels


@app.post('/hotels')
def add_hotel(
        title: str = Body(),
        name: str = Body()
):
    global hotels

    hotels.append({'id': hotels[-1]['id']+1,
                   'title': title,
                   'name': name
    })

    return {'status':'OK'}


@app.delete('/hotel/{hotel_id}')
def delete_hotel(
        hotel_id: int
):
    global hotels
    
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]

    return {'status':'OK'}


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Body(description='пенис'),
    name: str = Body(description='члены')
):
    global hotels

    hotels[hotel_id-1] = {'id': hotel_id, 'title': title, 'name': name}

    return {'status':'OK'}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(default=None, description='пенис'),
    name: str | None = Body(default=None, description='члены')    
):
    global hotels

    hotels[hotel_id-1] = {'id': hotel_id, 'title': title if title else hotels[hotel_id-1]['title'], 'name': name if name else hotels[hotel_id-1]['name']}

    return {'status':'OK'}
