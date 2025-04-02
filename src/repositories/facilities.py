
from sqlalchemy import select, insert, delete

from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    mapper = FacilityDataMapper

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacilityDataMapper

    async def set_facilities(
            self,
            room_id: int,
            facilities_ids: list[int]
    ):
        current_facilities_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
            )
        
        current_facilities_result = await self.session.execute(current_facilities_query)
        current_facilities = current_facilities_result.scalars().all()
        
        facilities_to_delete = list(set(current_facilities) - set(facilities_ids))
        facilities_to_add = list(set(facilities_ids) - set(current_facilities))

        if facilities_to_delete:
            stmt_facilities_delete = (
                delete(self.model)
                .filter(
                    self.model.facility_id.in_(facilities_to_delete)
                    ,self.model.room_id == room_id
                    )
                                      ) 
            await self.session.execute(stmt_facilities_delete)

        if facilities_to_add:
            stmt_facilities_add = (
                insert(self.model)
                .values(
                    [{"room_id":room_id, "facility_id":i} for i in facilities_to_add]
                    )
                )
            await self.session.execute(stmt_facilities_add)