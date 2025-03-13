from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository():
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_one_or_none(self,**filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def get_one(self,**filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self,data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        returned_result = await self.session.execute(add_data_stmt)
        return returned_result.scalars().one()
    

    async def edit(self, data: BaseModel, **filter_by):
        query_to_check = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query_to_check)
        number_of_hotels = len(result.all())

        if number_of_hotels == 0:
            return {'status':'404'}
        if number_of_hotels > 1:
            return {'status':'400'}

        edit_data_stmt = update(self.model).values(**data.model_dump()).filter_by(**filter_by)
        await self.session.execute(edit_data_stmt)
        return {'status':'OK'}


    async def delete(self, **filter_by):
        query_to_check = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query_to_check)
        number_of_hotels = len(result.all())

        if number_of_hotels == 0:
            return {'status':'404'}
        if number_of_hotels > 1:
            return {'status':'400'}
        
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
        return {'status':'OK'}
