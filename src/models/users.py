from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base

class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str | None] = mapped_column(None, String(100))
    last_name: Mapped[str | None] = mapped_column(None, String(100))
    username: Mapped[str | None] = mapped_column(None, String(30), unique=True)