from pydantic import BaseModel, Field, ConfigDict

class HotelAddPut(BaseModel):
    title: str
    location: str

    model_config = ConfigDict(from_attributes = True)

class Hotel(HotelAddPut):
    id: int

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)

    model_config = ConfigDict(from_attributes = True)
