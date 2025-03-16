from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserLogin, UserLoginForRequest
    
class UserRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(
        self,
        email: str
):
        query = select(self.model).filter_by(email = email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if user:
            return UserLogin.model_validate(user)
        return None