from pydantic import BaseModel, ConfigDict


class mdl:
    a = 123
    b = "1123"
    c = 3


a = {"a": 123, "b": "1123"}


class mdd(BaseModel):
    a: int
    b: str

    model_config = ConfigDict(from_attributes=True)


print(mdd.model_validate(a))
