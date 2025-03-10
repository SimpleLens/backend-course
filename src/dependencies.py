from fastapi import Depends, Query
from pydantic import BaseModel, Field
from typing import Annotated

class Pagination(BaseModel):
    page: int | None = Field(None, ge=1)
    per_page: int | None = Field(None,le=50)

pagination_dep = Annotated[Pagination, Depends()]