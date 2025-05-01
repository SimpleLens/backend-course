import logging

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from fastapi import HTTPException

from src.repositories.mappers.mappers import DataMapper
from src.exceptions import ObjectNotFoundException, ObjectAlreadyExists


class BaseRepository:
    model = None
    schema: BaseModel = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model)
        if filter:
            query = query.filter(*filter)
        if filter_by:
            query = query.filter_by(**filter_by)

        result = await self.session.execute(query)

        try:
            data = result.scalars().all()
        except NoResultFound:
            raise ObjectNotFoundException
        
        return [self.mapper.map_to_domen_entity(model) for model in data]
 


    async def get_all(self):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        data = result.scalars().one_or_none()

        if not data:
            return None
        
        return self.mapper.map_to_domen_entity(data)
  

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        try:
            data = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        
        return self.mapper.map_to_domen_entity(data)


    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        
        try:
            returned_result = await self.session.execute(stmt)
        except Exception as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                logging.error(f"Не удалось записать данные в базу, ошибка: {ex.orig.__cause__}")
                raise ObjectAlreadyExists from ex   
            else:
                logging.error(f"Не удалось записать данные в базу, необработанная ошибка: {ex.orig.__cause__}")
                raise ex
        
        return self.mapper.map_to_domen_entity(returned_result.scalars().one())


    async def add_bulk(self, data: list[BaseModel]):
        stmt = insert(self.model).values([i.model_dump() for i in data])
        await self.session.execute(stmt)


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query_to_check = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query_to_check)

        try:
            result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        edit_data_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
        )
        await self.session.execute(edit_data_stmt)


    async def delete(self, **filter_by):
        query_to_check = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query_to_check)
        
        try:
            result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)


    async def delete_bulk(self, data: list):
        query_to_check = select(self.model).filter(self.model.id.in_(data))
        result = await self.session.execute(query_to_check)

        try:
            result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        delete_data_stmt = delete(self.model).filter(self.model.id.in_(data))
        await self.session.execute(delete_data_stmt)
