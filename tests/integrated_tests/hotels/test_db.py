from src.schemas.hotels import HotelAddPut
from src.utils.db_manager import DBManager


async def test_db_hotels(db):
    hotel = HotelAddPut(title="Пенс", location="улица пениса 12")
    added = await db.hotels.add(hotel)
    await db.commit()
