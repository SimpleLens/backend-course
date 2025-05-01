from h11 import Response
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException

from src.exceptions import ObjectAlreadyExists, PasswordIsIncorrectException, UserAlreadyExistsException, UserDoesNotExistException
from src.schemas.users import UserAdd, UserAddForRequest, UserLoginForRequest
from src.services.base import BaseService
from src.config import settings


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"])

    def encode_jwt_token(self, data: dict):  # {user_id, email}
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def decode_jwt_token(self, token) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(411, detail="Невалидный токен аутентификации")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(411, detail="Истекший токен аутентификации")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_hashed_password(self, password):
        return self.pwd_context.hash(password)
    
    async def registration_user(self, user_data: UserAddForRequest):
        hashed_passsword = self.get_hashed_password(user_data.password)
        user_data_to_register = UserAdd(
            hashed_password=hashed_passsword, **user_data.model_dump(exclude="password")
        )

        try:
            added_user = await self.db.users.add(user_data_to_register)
        except ObjectAlreadyExists:
            raise UserAlreadyExistsException

        await self.db.commit()

        return added_user

    async def login(self, user_data: UserLoginForRequest, response: Response):
        user = await self.db.users.get_user_with_hashed_password(user_data.email)

        if not user:
            raise UserDoesNotExistException

        if not self.verify_password(user_data.password, user.hashed_password):
            raise PasswordIsIncorrectException
        
        access_token = self.encode_jwt_token({"user_id": user.id, "email": user.email})

        response.set_cookie("access_token", access_token)

        return user, access_token
    
    async def get_me(self, user_id: int):
        user_data = await self.db.users.get_one_or_none(id=user_id)
        return user_data

