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
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))
        if location :
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.lower()}%"))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
    

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data: Hotel):
        stmt = insert(HotelsOrm).values(**data.model_dump()).returning(HotelsOrm)
        result = await self.session.execute(stmt)
        hotel_returned = result.scalars().first()
        return {'id':hotel_returned.id, 'title': hotel_returned.title, 'location': hotel_returned.location}
    
