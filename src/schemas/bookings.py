from datetime import datetime    

from pydantic import BaseModel, ConfigDict

 
class BookingAddRequest(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
