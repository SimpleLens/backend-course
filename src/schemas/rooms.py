from pydantic import BaseModel, ConfigDict, Field


class RoomAddForRequest(BaseModel):
    title: str
    price: int
    description: str | None = Field(None)
    quantity: int


class RoomAdd(RoomAddForRequest):
    hotel_id: int 


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPut(RoomAddForRequest): ...


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    price: int | None = Field(None)
    description: str | None = Field(None)
    quantity: int | None = Field(None)