from datetime import date

from sqlalchemy import func, select

from src.models.rooms import RoomsModel
from src.models.bookings import BookingsModel
from src.database import engine

def rooms_ids_to_get(
        date_to: date,
        date_from: date,
        hotel_id: int | None = None
):
    rooms_count = (
                select(BookingsModel.room_id, func.count("*").label("rooms_booked"))
                .select_from(BookingsModel)
                .filter(BookingsModel.date_from <= date_to, BookingsModel.date_to >= date_from)
                .group_by(BookingsModel.room_id)
                .cte(name="rooms_count")
                )

    rooms_left_table = (
                select
                    (RoomsModel.id.label("room_id"), 
                    (RoomsModel.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
                    )
                .select_from(RoomsModel)
                .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
                .cte("rooms_left_table")
                )

    query_for_hotels = (select(RoomsModel.id)
                        .select_from(RoomsModel)
                        )
    
    if hotel_id:
        query_for_hotels = query_for_hotels.filter_by(hotel_id=hotel_id)


    query_for_hotels =  query_for_hotels.subquery(name="rooms_ids_for_hotel") 

                        
    rooms_to_get = (select(rooms_left_table.c.room_id)
                    .filter
                        (rooms_left_table.c.rooms_left > 0,
                        rooms_left_table.c.room_id.in_(query_for_hotels)
                        )
                    )

    return rooms_to_get