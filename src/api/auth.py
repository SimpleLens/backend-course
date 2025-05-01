from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserAddForRequest, UserAdd, UserLoginForRequest
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DbDep
from src.exceptions import ObjectAlreadyExists, PasswordIsIncorrectException, PasswordIsIncorrectHTTPException, UserAlreadyExistsException, UserAlreadyExistsHTTPException, UserDoesNotExistException, UserDoesNotExistHTTPException

router = APIRouter(prefix="/auth", tags=["Аутентификация, аутентификация и регистрация"])


@router.post("/register")
async def registration_user(Db: DbDep, user_data: UserAddForRequest):
    try:
        added_user = await AuthService(Db).registration_user(user_data=user_data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException

    return {"status": "OK", "user": added_user}


@router.post("/login")
async def login(Db: DbDep, user_data: UserLoginForRequest, response: Response):
    try:
        user, access_token = await AuthService(Db).login(user_data=user_data, response=response)
    except UserDoesNotExistException:
        raise UserDoesNotExistHTTPException
    except PasswordIsIncorrectException:
        raise PasswordIsIncorrectHTTPException

    return {"access_token": access_token, "user": user}


@router.get("/me")
async def get_me(Db: DbDep, UserIdDep: UserIdDep):
    user_data = await AuthService(Db).get_me(user_id=UserIdDep)
    return user_data


@router.post("/logout")
async def logout(Db: DbDep, response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
