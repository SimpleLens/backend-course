

from src.schemas.rooms import Room
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository

class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room
