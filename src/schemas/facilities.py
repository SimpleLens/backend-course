from pydantic import BaseModel, Field, ConfigDict

class Facility(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)

class FacilityAdd(BaseModel):
    title: str