from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import Facility


class RoomAddForRequest(BaseModel):
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithFacilities(Room):
    facilities: list[Facility]


class RoomPutRequest(RoomAddForRequest): ...


class RoomPut(BaseModel):
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    price: int | None = Field(None)
    description: str | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    price: int | None = Field(None)
    description: str | None = Field(None)
    quantity: int | None = Field(None)
