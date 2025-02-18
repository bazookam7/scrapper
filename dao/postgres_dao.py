from typing import List, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from dao.base_dao import BaseDao
from dao.models.base_model import BaseModel
from dao.query.base_query import BaseQuery

class Postgres_Dao(BaseDao):
    _engine = None
    _Session = None
    
    def __new__(cls):
        raise TypeError("This class cannot be instantiated directly. Use class methods instead.")
    
    @classmethod
    def get_connection_url(cls) -> str:
        return os.getenv("POSTGRES_CONNECTION_URL")
    
    @classmethod
    def __get_instance(cls):
        if not cls._engine:
            cls._engine = create_engine(cls.get_connection_url())
            cls._Session = sessionmaker(bind=cls._engine)
        return cls
    
    @classmethod
    def query_data(cls, query: BaseQuery) -> List[BaseModel]:
        cls.__get_instance()
        with cls._Session() as session:
            result = session.scalars(query.build())
            return list(result)
    
    @classmethod
    def insert_data(cls, data: BaseModel):
        cls.__get_instance()
        with cls._Session() as session:
            data = session.merge(data)
            session.commit()
            return data.id
    
    @classmethod
    def insert_data_bulk(cls, data: List[BaseModel]):
        cls.__get_instance()
        with cls._Session() as session:
            if not data:
                return
                
            table = data[0].__table__
            keys = [k.name for k in table.primary_key]
            
            stmt = insert(table).on_conflict_do_update(
                index_elements=keys,
                set_={
                    c.name: insert(table).excluded[c.name]
                    for c in table.c
                    if c.name not in keys
                }
            )
            session.execute(stmt, [item.__dict__ for item in data])
            session.commit()
    
    @classmethod
    def delete_data(cls, data: BaseModel):
        cls.__get_instance()
        with cls._Session() as session:
            session.delete(data)
            session.commit()
    
    @classmethod
    def delete_data_bulk(cls, data: List[BaseModel]):
        cls.__get_instance()
        with cls._Session() as session:
            if not data:
                return
            
            table = data[0].__table__
            keys = [k.name for k in table.primary_key]
            ids_to_delete = [getattr(item, keys[0]) for item in data]  # Assuming the first key is the ID
            
            stmt = table.delete().where(table.c[keys[0]].in_(ids_to_delete))
            session.execute(stmt)
            session.commit() 