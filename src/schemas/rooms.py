from pydantic import BaseModel, ConfigDict, Field


class RoomAddForRequest(BaseModel):
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int
    facilities_ids: list[int]


class RoomAdd(BaseModel):
    hotel_id: int 
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPut(RoomAddForRequest): ...

class RoomPatch(BaseModel):
    title: str | None = Field(None)
    price: int | None = Field(None)
    description: str | None = Field(None)
    quantity: int | None = Field(None)

class RoomPatchRequest(RoomAddForRequest):

    facilities_ids: list[int] | None = Field(None)

