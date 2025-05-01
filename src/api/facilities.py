import json

from fastapi import APIRouter, BackgroundTasks

from services.facilities import FacilitiesService
from src.api.dependencies import DbDep
from src.schemas.facilities import FacilityAdd
from fastapi_cache.decorator import cache
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=5)
async def get_all_facilities(Db: DbDep, bgtask: BackgroundTasks):

    facilities = await FacilitiesService(Db).get_all_facilities(bgtask=bgtask)

    return {"status": "OK", "data": facilities}


@router.post("")
async def add_facility(Db: DbDep, data: FacilityAdd):
    added_facility = await FacilitiesService(Db).add_facility(data=data)
    return {"status": "OK", "data": added_facility}
