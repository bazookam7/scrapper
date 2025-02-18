from typing import Any, Dict, Type, TypeVar

from dao.data_source import DataSource
from dao.models.base_model import BaseModel
from dao.query.base_query import BaseQuery

T = TypeVar('T', bound=BaseModel)

class MongoQuery(BaseQuery):
    _collection_name = None
    _model_class: Type[T] = None

    def __init__(self):
        if not self._collection_name:
            raise NotImplementedError("_collection_name must be set in child class")
        if not self._model_class:
            raise NotImplementedError("_model_class must be set in child class")
        self.query_filter = {}

    def with_filter(self, custom_filter: Dict[str, Any]):
        """Allow adding custom MongoDB filter"""
        self.query_filter.update(custom_filter)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Return the final query dictionary"""
        return {
            "collection_name": self._collection_name,
            "filter": self.query_filter
        }
    
    def by_id(self, id: str):
        """Query by _id field"""
        self.query_filter["_id"] = id
        return self
    
    def to_model(self, data: Dict[str, Any]) -> T:        
        return self._model_class.from_db(data) 