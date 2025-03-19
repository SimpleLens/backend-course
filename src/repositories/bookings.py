

from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking
from src.models.bookings import BookingsModel

class BookingsRepository(BaseRepository):
    model = BookingsModel
    schema = Booking