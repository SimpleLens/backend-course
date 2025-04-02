
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsModel
from src.schemas.rooms import Room
from src.models.rooms import RoomsModel
from src.schemas.users import User
from src.models.users import UsersModel
from src.schemas.bookings import Booking
from src.models.bookings import BookingsModel
from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesModel
from src.schemas.facilities import RoomFacility
from src.models.facilities import RoomsFacilitiesModel

class HotelDataMapper(DataMapper):
    db_model = HotelsModel
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsModel
    schema = Room


class UserDataMapper(DataMapper):
    db_model = UsersModel
    schema = User


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesModel
    schema = Facility

    
class BookingDataMapper(DataMapper):
    db_model = BookingsModel
    schema = Booking


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesModel
    schema = RoomFacility
