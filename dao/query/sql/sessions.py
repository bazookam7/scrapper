from dao.models.sql.sessions import Session
from dao.query.sql_query import SQLQuery

class SessionQuery(SQLQuery):
    _model_class = Session

    def by_user_id(self, user_id: int):
        self._sql_query = self._sql_query.where(self._model_class.user_id == user_id)
        return self