from pydantic import BaseModel, Field, ConfigDict

class User(BaseModel):
    id: int 
    email: str = Field(max_lenght=200)
    first_name: str | None = Field(None, max_lenght=100)
    last_name: str | None = Field(None,max_lenght=100)
    username: str | None = Field(None, max_lenght=30)

    model_config = ConfigDict(from_attributes=True)

class UserAddForRequest(BaseModel):
    email: str = Field(max_lenght=200)
    password: str = Field(max_lenght=200)
    first_name: str | None = Field(None, max_lenght=100)
    last_name: str | None = Field(None,max_lenght=100)
    username: str | None = Field(None, max_lenght=30)

class UserAdd(BaseModel):
    email: str = Field(max_lenght=200)
    hashed_password: str = Field(max_lenght=200)
    first_name: str | None = Field(None, max_lenght=100)
    last_name: str | None = Field(None,max_lenght=100)
    username: str | None = Field(None, max_lenght=30)

class UserLoginForRequest(BaseModel):
    email: str = Field(max_lenght=200)
    password: str = Field(max_lenght=200)

class UserLogin(User):
    hashed_password: str = Field(max_lenght=200)