import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.facilities import FacilitiesModel


class RoomsModel(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    price: Mapped[int]
    description: Mapped[str | None]
    quantity: Mapped[int]

    facilities: Mapped[list["FacilitiesModel"]] = relationship(
        back_populates="rooms", secondary="rooms_facilities"
    )
