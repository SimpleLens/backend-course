

from fastapi import BackgroundTasks
from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    async def get_all_facilities(self, bgtask: BackgroundTasks):
        facilities = await self.db.facilities.get_all()
        bgtask.add_task(test_task, "прив ку")
        return facilities
    
    async def add_facility(self, data: FacilityAdd):
        added_facility = await self.db.facilities.add(data)
        await self.db.commit()

        return added_facility