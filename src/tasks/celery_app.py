from celery import Celery

from src.config import settings


celery_inst = Celery("celery", broker=settings.REDIS_URL, include="src.tasks.tasks")

celery_inst.conf.beat_schedule = {
    "task1": {"task": "todays_checkin_bookings", "schedule": 5}
}
