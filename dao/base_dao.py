from threading import Lock
import threading
import os
from abc import ABC, abstractmethod

class BaseDao(ABC):
    _client = None
    _lock = Lock()
    
    def __new__(cls):
        raise TypeError("This class cannot be instantiated directly. Use class methods instead.")
    
    @classmethod
    @abstractmethod
    def get_connection_url(cls) -> str:
        """Each DAO implementation must provide its connection URL"""
        pass
    
    # @classmethod
    # @abstractmethod
    # def get_db_name(cls) -> str:
    #     """Each DAO implementation must provide its database name"""
    #     pass 