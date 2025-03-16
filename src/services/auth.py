from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException

from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"])

    def encode_jwt_token(self, data: dict): #{user_id, email}
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


    def decode_jwt_token(self, token) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(411,detail="Невалидный токен аутентификации")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    
    def get_hashed_password(self, password):
        return self.pwd_context.hash(password)
    