
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel

class FacilitiesRepository(BaseRepository):
    schema = Facility
    model = FacilitiesModel

class RoomsFacilitiesRepository(BaseRepository):
    schema = RoomFacility
    model = RoomsFacilitiesModel
