
from src.schemas.hotels import HotelAddPut
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

async def test_db_hotels():
    hotel = HotelAddPut(title = "Пенс", location= "улица пениса 12")
    async with DBManager(async_session_maker_null_pool) as session:
        added = await session.hotels.add(hotel)
        await session.commit()
        print(added)