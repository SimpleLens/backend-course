
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesModel

class FacilitiesRepository(BaseRepository):
    schema = Facility
    model = FacilitiesModel