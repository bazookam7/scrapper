from abc import ABC, abstractmethod, ABCMeta
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import DeclarativeBase  # Updated import
from dao.data_source import DataSource

# Create a custom metaclass that combines both ABCMeta and DeclarativeBase's metaclass
class ModelMeta(type(DeclarativeBase), ABCMeta):
    pass

# Use the custom metaclass when creating the Base
class Base(DeclarativeBase, metaclass=ModelMeta):
    pass

class BaseModel(ABC):
    """Interface defining required methods for all models"""
    @abstractmethod
    def __init__(self, id: Any):
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convert model to dictionary"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""
        pass

    @classmethod
    @abstractmethod
    def get_data_source(cls) -> DataSource:
        """Get the data source type for this model"""
        pass

    @classmethod
    @abstractmethod
    def from_db(cls, data: dict):
        """Create instance from database data"""
        pass

class SQLBaseModel(Base, BaseModel):
    """Base class specifically for SQL models"""
    __abstract__ = True
    __tablename__ = None

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, id: Any = None):
        if not self.__tablename__:
            raise NotImplementedError("__tablename__ must be set in child class")
        if id is not None:
            self.id = id
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at

    def to_dict(self) -> Dict:
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""
        instance = cls(data.get('id'))
        for column in cls.__table__.columns:
            if column.name in data and column.name != 'id':
                setattr(instance, column.name, data[column.name])
        return instance

    @classmethod
    def from_db(cls, data: dict):
        """Create instance from database data"""
        return cls.from_dict(data)

    @classmethod
    def get_data_source(cls) -> DataSource:
        """Get the data source type for this model"""
        return DataSource.POSTGRES

class MongoBaseModel(BaseModel):
    """Base class specifically for MongoDB models"""
    _collection_name = None

    def __init__(self, _id: Any):
        if not self._collection_name:
            raise NotImplementedError("_collection_name must be set in child class")
        self._id = _id
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
    
    def to_dict(self):
        # Get all instance attributes except _collection_name
        instance_dict = {
            key: value for key, value in vars(self).items() if key != "_collection_name"
        }
        
        return {
            "collection_name": self._collection_name,
            "item": instance_dict
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Generic method to create instance from dictionary"""
        return cls(**data)
    
    @classmethod
    def get_data_source(cls) -> DataSource:
        """
        Default to MongoDB, can be overridden by specific models
        """
        return DataSource.MONGO_DB



    def update(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now(timezone.utc)


    def populate_from_dict(self, data: dict):
        """Populate the instance from a dictionary"""
        for key, value in data.items():
            setattr(self, key, value)


    @classmethod
    def from_db(cls, data: dict):
        instance = cls.__new__(cls)
        # Populate all fields from  data store
        instance.populate_from_dict(data)
        return instance  