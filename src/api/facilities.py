from fastapi import APIRouter

from src.api.dependencies import DbDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_all_facilities(
        Db: DbDep
):
    return await Db.facilities.get_all()

@router.post("")
async def add_facility(
        Db: DbDep,
        data: FacilityAdd
):
    await Db.facilities.add(data)
    await Db.commit()
    return {"status":"OK"}