from dao.models.sql.user_query_logs import UserQueryLog
from dao.query.sql_query import SQLQuery
from sqlalchemy import and_
from sqlalchemy import desc  # Import desc for sorting


class UserQueryLogQuery(SQLQuery):
    _model_class = UserQueryLog

    def by_user_id(self, user_id: int):
        self._sql_query = self._sql_query.where(self._model_class.user_id == user_id)
        return self
    def by_date_range(self, start_date, end_date):
        self._sql_query = self._sql_query.where(
            and_(
                self._model_class.created_at >= start_date,
                self._model_class.created_at <= end_date
            )
        )
        return self 
    def sort_by_timestamp_desc(self):
        # Sort by timestamp in descending order
        self._sql_query = self._sql_query.order_by(desc(self._model_class.created_at))
        return self
    
    def by_parent_chat_id(self, parent_chat_id: str):
        self._sql_query = self._sql_query.where(self._model_class.parent_chat_id == parent_chat_id)
        return self

