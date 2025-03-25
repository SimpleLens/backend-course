from pydantic import BaseModel, Field, ConfigDict


class FacilityAdd(BaseModel):
    title: str

class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AddRoomFacility(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(AddRoomFacility):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
