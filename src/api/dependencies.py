from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker

class Pagination(BaseModel):
    page: int = Field(default=1,ge=1)
    per_page: int | None = Field(None,le=50)

pagination_dep = Annotated[Pagination, Depends()]

def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, detail="Вы не аутентифицированы")
    return token


def get_current_user_id(token: Annotated[str, Depends(get_access_token)]) -> int:
    decode_jwt = AuthService().decode_jwt_token(token)
    return decode_jwt["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]

async def getDB():
    async with DBManager(async_session_maker) as db:
        yield db

DbDep = Annotated[DBManager, Depends(getDB)]