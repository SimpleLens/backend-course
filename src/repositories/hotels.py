from sqlalchemy import select, insert, func

from src.models.hotels import HotelsOrm 
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsOrm


    def __init__(self, session):
        self.session = session


    async def get_all(self, title, location, limit, offset):
        query = select(HotelsOrm)

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        if location :
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
    