from typing import Any, Dict, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.sql import Select

from dao.data_source import DataSource
from dao.models.base_model import BaseModel
from dao.query.base_query import BaseQuery

T = TypeVar('T', bound=BaseModel)

class SQLQuery(BaseQuery):
    _model_class: Type[T] = None

    def __init__(self):
        if not self._model_class:
            raise NotImplementedError("_model_class must be set in child class")
        self._sql_query = select(self._model_class)

    @property
    def _table_name(self) -> str:
        """Return table name from model for compatibility with BaseQuery"""
        return self._model_class.__tablename__

    def build(self) -> Select:
        """Return the final SQLAlchemy query"""
        return self._sql_query
    
    def by_id(self, id: str):
        """Query by id field"""
        self._sql_query = self._sql_query.where(self._model_class.id == id)
        return self
    
    def to_model(self, data: T) -> T:
        return data 
    
    