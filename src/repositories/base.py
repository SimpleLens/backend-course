from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
from fastapi import HTTPException


class BaseRepository():
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model)
        if filter:
            query = (query
                    .filter(*filter)
                    )
        if filter_by:
            query = (query
                    .filter_by(**filter_by)
                    )

        result = await self.session.execute(query)
        result_after = result.scalars().all()

        if result_after:
            return [self.schema.model_validate(model) for model in result_after]
        else: 
            return None    


    async def get_all(self):
        return await self.get_filtered()
        

    async def get_one_or_none(self,**filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        result_after = result.scalars().one_or_none()
        if result_after:
            return self.schema.model_validate(result_after)
        else: 
            return None
    

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        result_after = result.scalars().one()
        if result_after:
            return self.schema.model_validate(result_after)
        else: 
            return None


    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        returned_result = await self.session.execute(add_data_stmt)
        return self.schema.model_validate(returned_result.scalars().one())


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query_to_check = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query_to_check)
        number_of_hotels = len(result.all())

        if number_of_hotels == 0:
            raise HTTPException(404, detail="Не найдено ни одной сущности")

        edit_data_stmt = update(self.model).values(**data.model_dump(exclude_unset=exclude_unset)).filter_by(**filter_by)
        await self.session.execute(edit_data_stmt)
        return {'status':'OK'}


    async def delete(self, **filter_by):
        query_to_check = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query_to_check)
        number_of_hotels = len(result.all())

        if number_of_hotels == 0:
            raise HTTPException(404, detail="Не найдено ни одной сущности")
        
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
        return {'status':'OK'}
