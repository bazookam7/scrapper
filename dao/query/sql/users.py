

from typing import List
from dao.models.sql.users import User
from dao.query.sql_query import SQLQuery


class UserQuery(SQLQuery):
    _model_class = User

    def by_username(self, username: str):
        self._sql_query = self._sql_query.where(self._model_class.username == username)
        return self

    def by_id(self, user_id: int):
        self._sql_query = self._sql_query.where(self._model_class.id == user_id)
        return self
    
    def by_ids(self, user_ids: List[int]):
        self._sql_query = self._sql_query.where(self._model_class.id.in_(user_ids))
        return self

