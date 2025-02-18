from dao.query.sql_query import SQLQuery
from dao.models.sql.document_permissions import DocumentPermissions

class DocumentPermissionsQuery(SQLQuery):
    _model_class = DocumentPermissions

    def by_document_id(self, document_id: str):
        self._sql_query = self._sql_query.where(self._model_class.document_id == document_id)
        return self

    def by_permission_id(self, permission_id: int):
        self._sql_query = self._sql_query.where(self._model_class.permission_id == permission_id)
        return self

    





