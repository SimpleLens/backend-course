from pydantic import BaseModel, Field, ConfigDict

class Hotel(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)
