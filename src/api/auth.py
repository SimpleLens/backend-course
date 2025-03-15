from fastapi import APIRouter
from passlib.context import CryptContext

from src.schemas.users import UserAddForRequest, UserAdd
from repositories.users import UserRepository
from src.database import async_session_maker

router = APIRouter(prefix='/auth', tags=["Аутентификация, аутентификация и регистрация"])

pwd_context = CryptContext(schemes=["bcrypt"])

@router.post("/register")
async def registration_user(
        user_data: UserAddForRequest
):
    hashed_passsword = pwd_context.hash(user_data.password)
    user_data_to_register = UserAdd(hashed_password=hashed_passsword, **user_data.model_dump())
    async with async_session_maker() as session:
        await UserRepository(session).add(user_data_to_register)
        await session.commit()