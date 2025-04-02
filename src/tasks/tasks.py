import time
import asyncio

from src.tasks.celery_app import celery_inst
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

#@celery_inst.task
def test_task(msg):
    time.sleep(5)
    print(msg)


async def get_todays_checkin_bookings():
    async with DBManager(async_session_maker_null_pool) as db:
        print(await db.bookings.get_bookings_with_todays_checkin())


@celery_inst.task(name="todays_checkin_bookings")
def send_email_todays_checkin_bookings():
    asyncio.run(get_todays_checkin_bookings())