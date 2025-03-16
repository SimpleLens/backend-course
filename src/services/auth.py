from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"])

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    
    def get_hashed_password(self, password):
        return self.pwd_context.hash(password)