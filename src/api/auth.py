from fastapi import APIRouter, HTTPException, Response, Request

from src.schemas.users import UserAddForRequest, UserAdd, UserLoginForRequest
from repositories.users import UserRepository
from src.database import async_session_maker
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep

router = APIRouter(prefix='/auth', tags=["Аутентификация, аутентификация и регистрация"])


@router.post("/register")
async def registration_user(
        user_data: UserAddForRequest
):
    hashed_passsword = AuthService().get_hashed_password(user_data.password)
    user_data_to_register = UserAdd(hashed_password=hashed_passsword, **user_data.model_dump(exclude="password"))
    async with async_session_maker() as session:
        added_user = await UserRepository(session).add(user_data_to_register)
        await session.commit()
    
    return {"status":"OK", "user":added_user}


@router.post("/login")
async def login(
    user_data: UserLoginForRequest,
    response: Response
):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_user_with_hashed_password(user_data.email)

    if not user: 
        raise HTTPException(status_code=401, detail="Пользователя не существует")
    
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    access_token = AuthService().encode_jwt_token({"user_id":user.id, "email":user.email})

    response.set_cookie("access_token", access_token)

    return {"access_token": access_token, "user": user}


@router.get("/me")
async def get_me(
        UserIdDep: UserIdDep
):
    async with async_session_maker() as session:
        user_data = await UserRepository(session).get_one_or_none(id = UserIdDep)
    return user_data

@router.post("/logout")
async def logout(
    response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK"}