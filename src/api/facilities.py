import json

from fastapi import APIRouter, BackgroundTasks

from src.api.dependencies import DbDep
from src.schemas.facilities import FacilityAdd
from fastapi_cache.decorator import cache
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
#@cache(expire=5)
async def get_all_facilities(
        Db: DbDep,
        bgtask: BackgroundTasks
):

    facilities = await Db.facilities.get_all()
    bgtask.add_task(test_task,"прив ку")
    return facilities

@router.post("")
async def add_facility(
        Db: DbDep,
        data: FacilityAdd
):
    await Db.facilities.add(data)
    await Db.commit()
    return {"status":"OK"}