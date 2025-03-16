from fastapi import APIRouter, HTTPException, Response, Request

from src.schemas.users import UserAddForRequest, UserAdd, UserLoginForRequest
from repositories.users import UserRepository
from src.database import async_session_maker
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=["Аутентификация, аутентификация и регистрация"])


@router.post("/register")
async def registration_user(
        user_data: UserAddForRequest
):
    hashed_passsword = AuthService().get_hashed_password(user_data.password)
    user_data_to_register = UserAdd(hashed_password=hashed_passsword, **user_data.model_dump())
    async with async_session_maker() as session:
        await UserRepository(session).add(user_data_to_register)
        await session.commit()


@router.post("/login")
async def login(
    user_data: UserLoginForRequest,
    response: Response
):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_user_with_hashed_password(user_data.email)

    if not user: 
        raise HTTPException(status_code=401, detail="Пользователя не существует")
    if not AuthService().verify_password(user_data.password,user.hashed_password):
         raise HTTPException(status_code=401, detail="Неверный пароль")

    access_token = AuthService().create_access_token({"id":user.id})

    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(
        request: Request
):
    access_token = request.cookies.get('access_token')
    print(access_token)