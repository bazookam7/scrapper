from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar, Union
from sqlalchemy.sql import Select

from dao.data_source import DataSource
from dao.models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseQuery(ABC):
    # @property
    # @abstractmethod
    # def _collection_name(self) -> str:
    #     pass

    @property
    @abstractmethod
    def _model_class(self) -> Type[T]:
        pass

    @abstractmethod
    def build(self) -> Any:
        """Return the final query"""
        pass

    @abstractmethod
    def by_id(self, id: str):
        """Query by id field"""
        pass
    
    @classmethod
    def get_data_source(cls) -> DataSource:
        """Get data source from model class"""
        return cls._model_class.get_data_source()
    
    @abstractmethod
    def to_model(self, data: Any) -> T:
        """Convert database result to model"""
        pass
    

