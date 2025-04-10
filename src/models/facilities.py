import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.rooms import RoomsModel


class FacilitiesModel(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    rooms: Mapped[list["RoomsModel"]] = relationship(
        back_populates="facilities", secondary="rooms_facilities"
    )


class RoomsFacilitiesModel(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
