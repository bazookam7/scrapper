from typing import List, Type
from dao.base_dao import BaseDao
from dao.data_source import DataSource
from dao.models.base_model import BaseModel
from dao.query.base_query import BaseQuery
from dao.postgres_dao import Postgres_Dao

class DaoFactory:
    _dao_registry = {
        DataSource.POSTGRES: Postgres_Dao,
    }

    @classmethod
    def get_dao(cls, model: Type[BaseModel]) -> BaseDao:
        """
        Returns appropriate DAO based on model's data source preference
        """
        data_source = model.get_data_source()
        if data_source not in cls._dao_registry:
            raise ValueError(f"No DAO implementation found for data source: {data_source}")
        
        return cls._dao_registry[data_source]

    @classmethod
    def get_dao(cls, query: Type[BaseQuery]) -> BaseDao:
        """
        Returns appropriate DAO based on model's data source preference
        """
        data_source = query.get_data_source()
        if data_source not in cls._dao_registry:
            raise ValueError(f"No DAO implementation found for data source: {data_source}")
        
        return cls._dao_registry[data_source]


    @classmethod
    def query_data(cls, query: Type[BaseQuery]) -> List[Type[BaseModel]]:
        if query is None:
            return
        dao = cls.get_dao(query)
        items= dao.query_data(query)
        return [query.to_model(item) for item in items]
    
    @classmethod
    def insert_data(cls, model: Type[BaseModel]):
        if model is None:
            return 
        dao = cls.get_dao(model)
        return dao.insert_data(model)
    
    @classmethod
    def insert_data_bulk(cls,model:List[Type[BaseModel]]):
        if model is None or len(model) == 0:
            return
        dao = cls.get_dao(model[0])
        return dao.insert_data_bulk(model)
    
    @classmethod
    def delete_data(cls, model: Type[BaseModel]):
        if model is None:
            return
        dao = cls.get_dao(model)
        return dao.delete_data(model)
    
    @classmethod
    def delete_data_bulk(cls, model: List[Type[BaseModel]]):
        if model is None or len(model) == 0:
            return
        dao = cls.get_dao(model[0])
        return dao.delete_data_bulk(model)

